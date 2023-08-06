#  Copyright (c) 2020.  Elizabeth Housden
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#  associated documentation files (the "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
#  following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial
#  portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
import os
import sys
import subprocess

import ghau.errors as ge
import ghau.files as gf
from github import Github, RateLimitExceededException, UnknownObjectException, GitRelease


def _find_release_asset(release: GitRelease.GitRelease, asset: str, debug: bool) -> str:  # TODO: detect asset use regex
    """Return the requested asset's download url from the given release.
    If no specific asset is requested, it will return the first one it comes across.

    :exception ghau.errors.ReleaseAssetError: No asset by given name was found.
    :exception ghau.errors.NoAssetsFoundError: No assets found for given release."""
    al = release.get_assets()
    if al.totalCount == 0:  # if there are no assets, abort.
        raise ge.NoAssetsFoundError(release.tag_name)
    if asset is None:  # if no specific asset is requested, download the first it finds.
        return al[0].browser_download_url
    for item in al:  # otherwise, look for the specific asset requested.
        if item.name == asset:
            gf.message("Found asset {} with URL: {}".format(item.name, item.browser_download_url), debug)
            return item.browser_download_url
        raise ge.ReleaseAssetError(release.tag_name, asset)  # no asset found by requested name? abort.


def _update_check(local, online):  # TODO Improve update detection, if it's newer, version number, etc.
    """Compares the given versions, returns True if the values are different."""
    x = True if online != local else False
    return x


def _load_release(repo: str, pre_releases: bool, auth) -> GitRelease.GitRelease:
    """Returns the latest release (or pre_release if enabled) for the loaded repository.

    :exception ghau.errors.ReleaseNotFoundError: No releases found for given repository.

    :exception ghau.errors.GithubRateLimitError: Hit the rate limit in the process of loading the release.

    :exception ghau.errors.RepositoryNotFoundError: Given repository is not found."""
    g = Github(auth)
    try:
        if g.get_repo(repo).get_releases().totalCount == 0:  # no releases found
            raise ge.ReleaseNotFoundError(repo)
        if pre_releases:
            return g.get_repo(repo).get_releases()[0]
        elif not pre_releases:
            for release in g.get_repo(repo).get_releases():
                if not release.prerelease:
                    return release
                raise(ge.ReleaseNotFoundError(repo))
    except RateLimitExceededException:
        reset_time = g.rate_limiting_resettime
        raise ge.GithubRateLimitError(reset_time)
    except UnknownObjectException:
        raise ge.RepositoryNotFoundError(repo)


def _run_cmd(command: str):
    """Run the given command and close the python interpreter.
    If no command is given, it will just close."""
    if command is None:  # closes program without reboot if no command is given.
        sys.exit()
    if sys.platform == "win32":  # windows needs special treatment
        data = command.split()
        subprocess.Popen(data)
        sys.exit()
    else:
        subprocess.Popen(command)
        sys.exit()


def python(file: str) -> str:  # used by users to reboot to the given python file in the working directory.
    """Builds the command required to run the given python file if it is in the current working directory.

    Useful for building the command to place in the reboot parameter of :class:`ghau.update.Update`.

    This is the recommended way to reboot into a python file, as it adds an argument ghau detects to stop update loops.
    This will also ensure the file given is a python script.

    See also: :func:`ghau.update.exe`, :func:`ghau.update.cmd`

    :exception ghau.errors.FileNotScriptError: raised if the given file is not a python script.
    """
    if file.endswith(".py"):
        executable = sys.executable
        file_path = os.path.join(os.getcwd(), file)
        return "{} {} -ghau".format(executable, file_path)
    else:
        raise ge.FileNotScriptError(file)


def exe(file: str) -> str:  # added for consistency. Boots file in working directory.
    """Added for consistency with ghau.update.python.

    Useful for building the command to place in the reboot parameter of :class:`ghau.update.Update`.

    This is the recommended way to reboot into an executable file, as it adds an argument ghau detects to stop update
    loops. This will also ensure the file given is an .exe file.

    See also: :func:`ghau.update.python`, :func:`ghau.update.cmd`

    :exception ghau.errors.FileNotExeError: raised if the given file is not an executable."""
    if file.endswith(".exe"):
        return "{} -ghau".format(file)
    else:
        raise ge.FileNotExeError(file)


def cmd(command: str) -> str:  # same as exe
    """Added for consistency with ghau.update.python.

    Useful for building the command to place in the reboot parameter of :class:`ghau.update.Update`.

    This is the recommended way to reboot using a command, as it adds an argument ghau detects to stop update loops.

    See also: :func:`ghau.update.python`, :func:`ghau.update.exe`
    """
    return "{} -ghau".format(command)


class Update:
    """Main class used to trigger updates through ghau.

    :param version: local version to check against online versions.
    :type version: str
    :param repo: github repository to check for updates in.
        Must be publicly accessible unless you are using a Github Token.
    :type repo: str
    :param pre-releases: accept pre-releases as valid updates, defaults to False.
    :type pre-releases: bool, optional
    :param reboot: command intended to reboot the program after a successful update installs.
    :type reboot: str, optional
    :param clean: clean directory before installing updates, defaults to False.
    :type clean: bool, optional
    :param download: the type of download you wish to use for updates.
        Either "zip" (source code) or "asset" (uploaded files), defaults to "zip".
    :type download: str, optional
    :param asset: name of asset to download when set to "asset" mode.
    :type asset: str, optional.
    :param auth: authentication token used for accessing the Github API, defaults to None.
    :type auth: str, optional
    :param ratemin: minimum amount of API requests left before updates will stop, defaults to 20.
        Maximum is 60/hr for unauthorized requests, and 5000 for authorized requests.
    :type ratemin: int, optional.
    :param debug: receive debug messages regarding the update process, defaults to False.
    :type debug: bool, optional.
    """
    def __init__(self, version: str, repo: str, pre_releases: bool = False,
                 reboot: str = None, clean: bool = False, download: str = "zip",
                 asset: str = None, auth: str = None, ratemin: int = 20, debug: bool = False):
        self.auth = auth
        self.ratemin = ratemin
        self.debug = debug
        self.version = version
        self.repo = repo
        self.pre_releases = pre_releases
        self.clean = clean
        self.whitelist = []
        self.reboot = reboot
        self.download = download
        self.asset = asset

    def update(self):
        """Check for updates and install if an update is found.

        All expected exceptions triggered during the run of this method are automatically handled.
        They are intentionally raised to stop the update process should it be needed, not the entire program.

        An error message will be printed to the console summarizing what occurred when this happens.

        :exception ghau.errors.InvalidDownloadTypeError: an unexpected value was given to the download parameter of
            :class:`ghau.update.Update`."""
        try:
            ge.argtest(sys.argv, "-ghau")
            ge.devtest(os.path.realpath(os.path.dirname(sys.argv[0])))
            ge.ratetest(self.ratemin, self.auth)
            latest_release = _load_release(self.repo, self.pre_releases, self.auth)
            do_update = _update_check(self.version, latest_release.tag_name)
            if do_update:
                wl = gf.load_whitelist(os.path.realpath(os.path.dirname(sys.argv[0])), self.whitelist, self.debug)
                gf.clean_files(wl, self.clean, self.debug)
                if self.download == "zip":
                    gf.download(latest_release.zipball_url, "update.zip", self.debug)
                    gf.extract_zip(os.path.realpath(os.path.dirname(sys.argv[0])), "update.zip")
                    gf.message("Updated from {} to {}".format(self.version, latest_release.tag_name), True)
                    _run_cmd(self.reboot)
                    sys.exit()
                if self.download == "asset":
                    asset_link = _find_release_asset(latest_release, self.asset, self.debug)
                    gf.download(asset_link, self.asset, self.debug)
                    gf.message("Updated from {} to {}".format(self.version, latest_release.tag_name), True)
                    _run_cmd(self.reboot)
                    sys.exit()
                else:
                    raise ge.InvalidDownloadTypeError(self.download)
            else:
                gf.message("No update required.", True)
        except (ge.GithubRateLimitError, ge.GitRepositoryFoundError, ge.ReleaseNotFoundError, ge.ReleaseAssetError,
                ge.FileNotExeError, ge.FileNotScriptError, ge.NoAssetsFoundError, ge.InvalidDownloadTypeError,
                ge.LoopPreventionError) as e:
            gf.message(e.message, True)
            return

    def whitelist_test(self):
        """Test the whitelist and output what isn't protected.

        Useful for testing your whitelist configuration."""
        gf.message(self.whitelist, self.debug)
        pl = gf.load_whitelist(os.path.realpath(os.path.dirname(sys.argv[0])), self.whitelist, self.debug)
        gf.message(pl, self.debug)
        if len(pl) == 0:
            gf.message("Everything is protected by your whitelist", True)
        else:
            gf.message("Whitelist will not protect the following: ", True)
            for path in pl:
                gf.message(path, True)

    def wl_folder(self, *args: str):
        """Add folders to the whitelist. This protects any listed folders from deletion during update installation.
        Each folder should be a string referring to its name.

        :param args: list of folders to protect.
        :type args: str

        >>> self.wl_folder("/data", "*/docs")"""
        for arg in args:
            self.whitelist.append({arg: True})
            gf.message("Loaded folder {} into the whitelist.".format(arg), self.debug)

    def wl_file(self, *args: str):
        """Add files to the whitelist. This protects any listed files from deletion during update installation.
        Each file should be a string referring to its name.

        :param args: list of files to protect.
        :type args: str

        >>> self.wl_file("data.*", "*.txt")"""
        for arg in args:
            self.whitelist.append({arg: False})
            gf.message("Loaded file {} into the whitelist.".format(arg), self.debug)
