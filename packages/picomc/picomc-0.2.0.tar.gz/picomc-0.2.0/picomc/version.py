import json
import operator
import os
import posixpath
import re
import sys
import urllib.parse
import urllib.request
from functools import reduce
from platform import architecture

import click
import requests
from picomc.downloader import DownloadQueue
from picomc.globals import platform, vm
from picomc.logging import logger
from picomc.utils import cached_property, file_sha1, get_filepath


class VersionType:
    MAP = {"release": 1, "snapshot": 2, "old_alpha": 4, "old_beta": 8}

    def __init__(self, d=None):
        if isinstance(d, int):
            self._a = d
        elif isinstance(d, str):
            self._a = self.MAP[d]

    def __or__(self, other):
        return VersionType(self._a | other._a)

    def match(self, s):
        return bool(self.MAP[s] & self._a)

    @staticmethod
    def create(release, snapshot, alpha, beta):
        a = release | (2 * snapshot) | (4 * alpha) | (8 * beta)
        return VersionType(a)


VersionType.RELEASE = VersionType("release")
VersionType.SNAPSHOT = VersionType("snapshot")
VersionType.ALPHA = VersionType("old_alpha")
VersionType.BETA = VersionType("old_beta")

MODE_OVERRIDE = 0
MODE_REDUCE = 1


class CachedVspecAttr(object):
    def __init__(self, attr, mode=MODE_OVERRIDE, reduce_func=None, default=None):
        self.attr = attr
        self.mode = mode
        self.rfunc = reduce_func
        self.default = default

    def __get__(self, vspec, cls):
        if vspec is None:
            return self
        try:
            if self.mode == MODE_OVERRIDE:
                for v in vspec.chain:
                    if self.attr in v.raw_vspec:
                        r = v.raw_vspec[self.attr]
                        break
                else:
                    raise AttributeError()
            elif self.mode == MODE_REDUCE:
                try:
                    r = reduce(
                        self.rfunc,
                        (
                            v.raw_vspec[self.attr]
                            for v in vspec.chain[::-1]
                            if self.attr in v.raw_vspec
                        ),
                    )
                except TypeError as e:
                    raise AttributeError() from e
        except AttributeError as e:
            if self.default is not None:
                r = self.default(vspec.vobj)
        finally:
            try:
                setattr(vspec, self.attr, r)
                return r
            except UnboundLocalError as e:
                raise AttributeError() from e


def argumentadd(d1, d2):
    d = d1.copy()
    for k, v in d2.items():
        if k in d:
            d[k] += v
        else:
            d[k] = v
    return d


class VersionSpec:
    def __init__(self, vobj):
        self.vobj = vobj
        self.chain = self._resolve_chain()

    def _resolve_chain(self):
        chain = []
        chain.append(self.vobj)
        cv = self.vobj
        while "inheritsFrom" in cv.raw_vspec:
            cv = Version(cv.raw_vspec["inheritsFrom"])
            chain.append(cv)
        return chain

    minecraftArguments = CachedVspecAttr("minecraftArguments")
    arguments = CachedVspecAttr("arguments", mode=MODE_REDUCE, reduce_func=argumentadd)
    mainClass = CachedVspecAttr("mainClass")
    assetIndex = CachedVspecAttr("assetIndex")
    libraries = CachedVspecAttr("libraries", mode=MODE_REDUCE, reduce_func=operator.add)
    jar = CachedVspecAttr("jar", default=lambda vobj: vobj.version_name)
    downloads = CachedVspecAttr("downloads", default=lambda vobj: {})


class Version:
    LIBRARIES_URL = "https://libraries.minecraft.net/"
    ASSETS_URL = "http://resources.download.minecraft.net/"

    def __init__(self, version_name):
        self.version_name = version_name

    @cached_property
    def jarfile(self):
        v = self.vspec.jar
        return get_filepath("versions", v, "{}.jar".format(v))

    @cached_property
    def raw_vspec(self):
        fpath = get_filepath(
            "versions", self.version_name, "{}.json".format(self.version_name)
        )
        ver = vm.get_manifest_version(self.version_name)
        if not ver:
            raise ValueError("Specified version not available.")
        url = ver["url"]
        # Pull the hash out of the url. This is prone to breakage, maybe
        # just try to download the vspec and don't care about whether it
        # is up to date or not.
        url_split = urllib.parse.urlsplit(url)
        sha1 = posixpath.basename(posixpath.dirname(url_split.path))
        if os.path.exists(fpath) and file_sha1(fpath) == sha1:
            logger.debug("Using cached vspec files, hash matches manifest")
            with open(fpath) as fp:
                return json.load(fp)

        try:
            logger.debug("Downloading vspec file")
            raw = requests.get(url).content
            dirpath = os.path.dirname(fpath)
            os.makedirs(dirpath, exist_ok=True)
            with open(fpath, "wb") as fp:
                fp.write(raw)
            j = json.loads(raw)
            return j
        except requests.ConnectionError:
            logger.error(
                "Failed to retrieve version json file. Check your internet connection."
            )
            sys.exit(1)

    @cached_property
    def vspec(self):
        return VersionSpec(self)

    @cached_property
    def raw_asset_index(self):
        iid = self.vspec.assetIndex["id"]
        url = self.vspec.assetIndex["url"]
        sha1 = self.vspec.assetIndex["sha1"]
        fpath = get_filepath("assets", "indexes", "{}.json".format(iid))
        if os.path.exists(fpath) and file_sha1(fpath) == sha1:
            logger.debug("Using cached asset index, hash matches vspec")
            with open(fpath) as fp:
                return json.load(fp)
        try:
            logger.debug("Downloading new asset index")
            raw = requests.get(url).content
            with open(fpath, "wb") as fp:
                fp.write(raw)
            return json.loads(raw)
        except requests.ConnectionError:
            logger.error("Failed to retrieve asset index.")
            sys.exit(1)

    def _libraries(self, natives_only=False):
        # The rule matching in this function could be cached,
        # not sure if worth it.
        for lib in self.vspec.libraries:
            rules = lib.get("rules", [])
            allow = "rules" not in lib
            for rule in rules:
                osmatch = True
                if "os" in rule:
                    osmatch = rule["os"]["name"] == platform
                if osmatch:
                    allow = rule["action"] == "allow"
            if not allow:
                continue
            if natives_only and "natives" not in lib:
                continue
            yield lib

    @staticmethod
    def _resolve_library(lib):
        # TODO
        # For some reason I don't remember, we are constructing the paths
        # to library downloads manually instead of using the url and hash
        # provided in the vspec. This should probably be reworked and hashes
        # should be checked instead of just the filenames
        suffix = ""
        if "natives" in lib:
            if platform in lib["natives"]:
                suffix = "-" + lib["natives"][platform]
                # FIXME this is an ugly hack
                suffix = suffix.replace("${arch}", architecture()[0][:2])
            else:
                logger.warn(
                    (
                        "Native library ({}) not available"
                        "for current platform ({}). Ignoring."
                    ).format(lib["name"], platform)
                )
                return None
        fullname = lib["name"]
        url_base = lib.get("url", Version.LIBRARIES_URL)
        p, n, v, *va = fullname.split(":")
        v2 = "-".join([v] + va)

        # TODO this is fugly
        class LibPaths:
            package = p.replace(".", "/")
            name = n
            version = v
            ext_version = v2
            filename = "{}-{}{}.jar".format(name, ext_version, suffix)
            fullpath = "{}/{}/{}/{}".format(package, name, version, filename)
            url = urllib.parse.urljoin(url_base, fullpath)
            basedir = get_filepath("libraries")
            local_relpath = os.path.join(*fullpath.split("/"))
            local_abspath = os.path.join(basedir, local_relpath)

        return LibPaths

    def lib_filenames(self, natives=False):
        for lib in self._libraries(natives):
            if not natives and "natives" in lib:
                continue
            paths = self._resolve_library(lib)
            if not paths:
                continue
            yield paths.local_abspath

    def download_jarfile(self, force=False):
        """Checks existence and hash of cached jar. Downloads a new one
        if either condition is violated."""
        logger.debug("Attempting to use jarfile: {}".format(self.jarfile))
        dlspec = self.vspec.downloads.get("client", None)
        if not dlspec:
            logger.debug("jarfile not in dlspec, skipping hash check.")
            if not os.path.exists(self.jarfile):
                logger.error("Jarfile does not exist and can not be downloaded.")
                raise RuntimeError()
            return

        logger.debug("Checking jarfile.")
        if (
            force
            or not os.path.exists(self.jarfile)
            or file_sha1(self.jarfile) != dlspec["sha1"]
        ):
            logger.info("Downloading jar ({}).".format(self.version_name))
            urllib.request.urlretrieve(dlspec["url"], self.jarfile)

    def download_libraries(self, force=False):
        """Downloads missing libraries."""
        logger.info("Checking libraries.")
        q = DownloadQueue()
        for lib in self._libraries():
            paths = self._resolve_library(lib)
            if not paths:
                continue
            if force or not os.path.exists(paths.local_abspath):
                q.add(paths.url, paths.local_relpath)
        q.download(paths.basedir)

    def download_assets(self, force=False):
        """Downloads missing assets."""
        # Produce reverse dict, as multiple files with a single hash
        # can exist and should only be downloaded once.
        rev = dict()
        for name, obj in self.raw_asset_index["objects"].items():
            h = obj["hash"]
            if h in rev:
                rev[h].append(name)
            else:
                rev[h] = [name]

        logger.info("Checking {} assets.".format(len(rev.keys())))

        is_virtual = self.raw_asset_index.get("virtual", False)

        q = DownloadQueue()
        for digest, names in rev.items():
            # This is a mess, should be rewritten. FIXME
            fname = os.path.join("objects", digest[0:2], digest)
            vfnames = (
                os.path.join("virtual", "legacy", *name.split("/")) for name in names
            )
            fullfname = get_filepath("assets", "objects", digest[0:2], digest)
            url = urllib.parse.urljoin(
                self.ASSETS_URL, "{}/{}".format(digest[0:2], digest)
            )
            outs = []
            # FIXME: probably should be checking hashes here...
            if force or not os.path.exists(fullfname):
                outs.append(fname)
            if is_virtual:
                for vfname in vfnames:
                    if force or not os.path.exists(
                        get_filepath("assets", *vfname.split("/"))
                    ):
                        outs.append(vfname)
            if outs:
                q.add(url, *outs)

        logger.info("Downloading {} assets. This could take a while.".format(len(q)))

        q.download(get_filepath("assets"))

    def prepare(self):
        self.download_jarfile()
        self.download_libraries()
        self.download_assets()


class VersionManager:
    VERSION_MANIFEST_URL = (
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    )

    def resolve_version_name(self, v):
        """Takes a metaversion and resolves to a version."""
        if v == "latest":
            v = self.manifest["latest"]["release"]
            logger.info("Resolved latest -> {}".format(v))
        elif v == "snapshot":
            v = self.manifest["latest"]["snapshot"]
            logger.info("Resolved snapshot -> {}".format(v))
        return v

    @cached_property
    def manifest(self):
        manifest_filepath = get_filepath("versions", "manifest.json")
        try:
            m = requests.get(self.VERSION_MANIFEST_URL).json()
            with open(manifest_filepath, "w") as mfile:
                json.dump(m, mfile, indent=4, sort_keys=True)
            return m
        except requests.ConnectionError:
            logger.warn(
                "Failed to retrieve version_manifest. "
                "Check your internet connection."
            )
            try:
                with open(manifest_filepath) as mfile:
                    logger.warn("Using cached version_manifest.")
                    return json.load(mfile)
            except FileNotFoundError:
                logger.warn("Cached version manifest not available.")
                raise RuntimeError("Failed to retrieve version manifest.")

    def get_manifest_version(self, version_name):
        for ver in self.manifest["versions"]:
            if ver["id"] == version_name:
                return ver

    def version_list(self, vtype=VersionType.RELEASE, local=False):
        r = [v["id"] for v in self.manifest["versions"] if vtype.match(v["type"])]
        if local:
            import os

            r += (
                "{} [local]".format(name)
                for name in os.listdir(get_filepath("versions"))
                if os.path.isdir(get_filepath("versions", name))
            )
        return r

    def get_version(self, version_name):
        return Version(self.resolve_version_name(version_name))


g_vobj = None


@click.group()
@click.argument("version_name")
def version_cli(version_name):
    """Operate on local Minecraft versions."""
    global g_vobj
    g_vobj = vm.get_version(version_name)


@click.command()
@click.option("--release", is_flag=True, default=False)
@click.option("--snapshot", is_flag=True, default=False)
@click.option("--alpha", is_flag=True, default=False)
@click.option("--beta", is_flag=True, default=False)
@click.option("--local", is_flag=True, default=False)
@click.option("--all", is_flag=True, default=False)
def list_versions(release, snapshot, alpha, beta, local, all):
    """List available Minecraft versions."""
    if all:
        release = snapshot = alpha = beta = local = True
    elif not (release or snapshot or alpha or beta):
        logger.info(
            "Showing only locally installed versions. "
            "Use `version list --help` to get more info."
        )
        local = True
    T = VersionType.create(release, snapshot, alpha, beta)
    print("\n".join(vm.version_list(vtype=T, local=local)))


@version_cli.command()
def prepare():
    g_vobj.prepare()


@version_cli.command()
@click.argument("which", default="client")
@click.option("--output", default=None)
def jar(which, output):
    """Download the file and save."""
    dlspec = g_vobj.vspec.downloads.get(which, None)
    if not dlspec:
        logger.error("No such dlspec exists for version {}".format(g_vobj.version_name))
        sys.exit(1)
    url = dlspec["url"]
    sha1 = dlspec["sha1"]
    ext = posixpath.basename(urllib.parse.urlsplit(url).path).split(".")[-1]
    if output is None:
        output = "{}_{}.{}".format(g_vobj.version_name, which, ext)
    if os.path.exists(output):
        logger.error("Refusing to overwrite {}".format(output))
        sys.exit(1)
    logger.info("Hash should be {}".format(sha1))
    logger.info("Downloading the {} file and saving to {}".format(which, output))
    urllib.request.urlretrieve(dlspec["url"], output)
    if file_sha1(output) != sha1:
        logger.warn("Hash of downloaded file does not match")


def register_version_cli(root_cli):
    root_cli.add_command(version_cli, "version")
    root_cli.add_command(list_versions)
