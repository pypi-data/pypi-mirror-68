import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

import os
import logging
from steam.enums import EResult
from steam.client import SteamClient
from steam.client.cdn import CDNClient, CDNDepotManifest, CDNDepotFile
from steam.exceptions import SteamError
from steam.core.crypto import sha1_hash

from steamctl.utils.format import fmt_size
from steamctl.utils.storage import (UserCacheFile, UserDataFile,
                                    UserCacheDirectory, UserDataDirectory,
                                    ensure_dir, sanitizerelpath
                                    )

cred_dir = UserDataDirectory('client')

class CachingSteamClient(SteamClient):
    credential_location = cred_dir.path

    def __init__(self, *args, **kwargs):
        if not cred_dir.exists():
            cred_dir.mkdir()
        SteamClient.__init__(self, *args, **kwargs)
        _LOG = logging.getLogger('CachingSteamClient')
        self._bootstrap_cm_list_from_file()

    def _handle_login_key(self, message):
        SteamClient._handle_login_key(self, message)

        with UserDataFile('client/%s.key' % self.username).open('w') as fp:
            fp.write(self.login_key)

    def get_cdnclient(self):
        return CachingCDNClient(self)

    def login_from_args(self, args, print_status=True):
        result = None

        # anonymous login
        if args.anonymous and not args.user:
            self._LOG.info("Attempting anonymous login")
            return self.anonymous_login()

        # user login
        user = args.user
        lastFile = UserDataFile('client/lastuser')

        # check for previously used user
        if not user and lastFile.exists():
            user = lastFile.read_text()

            if user:
                self._LOG.info("Reusing previous username: %s", user)
                self._LOG.info("Hint: use 'steamctl --user <username> ...' to change")
            else:
                self._LOG.debug("lastuser file is empty?")
                lastFile.remove()

        if user:
            # attempt login
            self.username = user

            # check for userkey and login without a prompt
            userkey =  UserDataFile('client/%s.key' % self.username)
            if userkey.exists():
                self._LOG.info("Attempting login with remembered credentials")
                self.login_key = userkey.read_text()
                result = self.relogin()

                if result == EResult.InvalidPassword:
                    self._LOG.info("Remembered credentials have expired")
                    userkey.remove()
                else:
                    return result

            self.sleep(0.1)

        # attempt manual cli login
        if not self.logged_on:
            if self.username:
                self._LOG.info("Enter credentials for: %s", self.username)
            else:
                self._LOG.info("Enter Steam login")

            result = self.cli_login(self.username)

        if not lastFile.exists() or lastFile.read_text() != self.username:
            lastFile.write_text(self.username)

        return result


class CTLDepotFile(CDNDepotFile):
    _LOG = logging.getLogger('CTLDepotFile')

    def download_to(self, target, no_make_dirs=False, pbar=None, verify=True):
        relpath = sanitizerelpath(self.filename)

        if no_make_dirs:
            relpath = os.path.basename(relpath)

        relpath = os.path.join(target, relpath)

        filepath = os.path.abspath(relpath)
        ensure_dir(filepath)

        checksum = self.file_mapping.sha_content.hex()

        # don't bother verifying if file doesn't already exist
        if not os.path.exists(filepath):
            verify = False

        with open(filepath, 'r+b' if verify else 'wb') as fp:
            fp.seek(0, 2)

            # pre-allocate space
            if fp.tell() != self.size:
                newsize = fp.truncate(self.size)

                if newsize != self.size:
                    raise SteamError("Failed allocating space for {}".format(filepath))

            self._LOG.info('{} {}  ({}, sha1:{})'.format(
                               'Verifying' if verify else 'Downloading',
                               relpath,
                               fmt_size(self.size),
                               checksum
                               ))

            fp.seek(0)
            for chunk in self.chunks:
                # verify chunk sha hash
                if verify:
                    cur_data = fp.read(chunk.cb_original)

                    if sha1_hash(cur_data) == chunk.sha:
                        if pbar:
                            pbar.update(chunk.cb_original)
                        continue

                    fp.seek(chunk.offset)  # rewind before write

                # download and write chunk
                data = self.manifest.cdn_client.get_chunk(
                                self.manifest.app_id,
                                self.manifest.depot_id,
                                chunk.sha.hex(),
                                )

                fp.write(data)

                if pbar:
                    pbar.update(chunk.cb_original)

class CTLDepotManifest(CDNDepotManifest):
    DepotFileClass = CTLDepotFile


class CachingCDNClient(CDNClient):
    DepotManifestClass = CTLDepotManifest
    _LOG = logging.getLogger('CachingCDNClient')

    def __init__(self, *args, **kwargs):
        CDNClient.__init__(self, *args, **kwargs)

        # load the cached depot decryption keys
        self.depot_keys.update(self.get_cached_depot_keys())

    def get_cached_depot_keys(self):
        return {int(depot_id): bytes.fromhex(key)
                for depot_id, key in (UserDataFile('depot_keys.json').read_json() or {}).items()
                }

    def save_cache(self):
        cached_depot_keys = self.get_cached_depot_keys()

        if cached_depot_keys == self.depot_keys:
            return

        self.depot_keys.update(cached_depot_keys)
        out = {str(depot_id): key.hex()
               for depot_id, key in self.depot_keys.items()
               }

        UserDataFile('depot_keys.json').write_json(out)

    def check_for_changes(self):
        changefile = UserCacheFile('last_change_number')
        change_number = 0

        if changefile.exists():
            try:
                change_number = int(changefile.read_text())
            except:
                changefile.remove()

        self._LOG.debug("Checking PICS for app changes")
        resp = self.steam.get_changes_since(change_number, True, False)

        if resp.force_full_app_update:
            change_number = 0

        if resp.current_change_number != change_number:
            with changefile.open('w') as fp:
                fp.write(str(resp.current_change_number))

            changed_apps = set((entry.appid for entry in resp.app_changes))

            if change_number == 0 or changed_apps:
                self._LOG.debug("Checking for outdated cached appinfo files")

                for appinfo_file in UserCacheDirectory('appinfo').iter_files('*.json'):
                    app_id = int(appinfo_file.filename[:-5])

                    if change_number == 0 or app_id in changed_apps:
                        appinfo_file.remove()

    def get_app_access_token(self, app_id):
        tokens = self.steam.get_access_tokens([app_id])

        if not tokens:
            self._LOG.debug("Access token request time out")
            return

        token = tokens['apps'][app_id]
        self._LOG.debug("Got access token %s for app %s", repr(token), app_id)
        return token

    def get_app_depot_info(self, app_id):
        if app_id not in self.app_depots:
            cached_appinfo = UserCacheFile("appinfo/{}.json".format(app_id))
            appinfo = None

            if cached_appinfo.exists():
                appinfo = cached_appinfo.read_json()

            if not appinfo:
                app_req = {'appid': app_id}
                token = self.get_app_access_token(app_id)

                if token:
                    app_req['access_token'] = token

                appinfo = self.steam.get_product_info([app_req])['apps'][app_id]

                if appinfo['_missing_token']:
                    raise SteamError("No access token available")

                cached_appinfo.write_json(appinfo)

            self.app_depots[app_id] = appinfo.get('depots', {})

        return self.app_depots[app_id]

    def get_cached_manifest(self, app_id, depot_id, manifest_gid):
        key = (app_id, depot_id, manifest_gid)

        if key in self.manifests:
            return self.manifests[key]

        # if we don't have the manifest loaded, check cache
        cached_manifest = UserCacheFile("manifests/{}_{}_{}".format(app_id, depot_id, manifest_gid))

        # we have a cached manifest file, load it
        if cached_manifest.exists():
            with cached_manifest.open('r+b') as fp:
                try:
                    manifest = self.DepotManifestClass(self, app_id, fp.read())
                except Exception as exp:
                    self._LOG.debug("Error parsing cached manifest: %s", exp)
                else:
                    # if its not empty, load it
                    if manifest.gid > 0:
                        self.manifests[key] = manifest

                        # update cached file if we have depot key for it
                        if manifest.filenames_encrypted and manifest.depot_id in self.depot_keys:
                            manifest.decrypt_filenames(self.depot_keys[manifest.depot_id])
                            fp.seek(0)
                            fp.write(manifest.serialize(compress=False))
                            fp.truncate()

                        return manifest

            # empty manifest files shouldn't exist, handle it gracefully by removing the file
            if key not in self.manifests:
                self._LOG.debug("Found cached manifest, but encountered error or file is empty")
                cached_manifest.remove()

    def is_manifest_cached(self, app_id, depot_id, manifest_gid):
        return self.get_cached_manifest(app_id, depot_id, manifest_gid) is not None

    def get_manifest(self, app_id, depot_id, manifest_gid, decrypt=True):
        key = (app_id, depot_id, manifest_gid)
        cached_manifest = UserCacheFile("manifests/{}_{}_{}".format(*key))

        if key not in self.manifests:
            self.get_cached_manifest(*key)

        # if we still dont have a manifest, load it from CDN
        if key not in self.manifests:
            manifest = CDNClient.get_manifest(self, app_id, depot_id, manifest_gid, decrypt)

            # cache the manifest
            with cached_manifest.open('wb') as fp:
                # if we have the key decrypt the manifest before caching
                if manifest.filenames_encrypted and manifest.depot_id in self.depot_keys:
                    manifest = self.DepotManifestClass(self, manifest.app_id, manifest.serialize(compress=False))
                    manifest.decrypt_filenames(self.depot_keys[manifest.depot_id])

                fp.write(manifest.serialize(compress=False))

        return self.manifests[key]
