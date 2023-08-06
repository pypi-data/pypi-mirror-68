#  Copyright (c) 2020.  InValidFire
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

import os
import shutil
import zipfile

import requests
from wcmatch import wcmatch


def message(msg, send: bool = False):  # TODO: Change to utilize 'logging' module, much more flexible.
    """Sends a message to the console if send is true. Used to easily control debug and error message output."""
    if send:
        print("GHAU: "+str(msg))


def download(url: str, save_file: str, debug: bool):
    """Download a file from the given url and save it to the given save_file."""
    r = requests.get(url, stream=True)
    with open(save_file, "wb") as fd:
        i = 0
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                i += 1
                fd.write(chunk)
                message("Wrote chunk {} to {}".format(str(i), save_file), debug)


def extract_zip(extract_path, file_path):  # TODO: Add whitelist filter, keep from overwriting protected files.
    """Extracts files from the given zip file_path into the given extract_path and performs cleanup operations."""
    with zipfile.ZipFile(file_path, "r") as zf:
        zf.extractall(extract_path)
        for item in zf.infolist():
            if item.is_dir():
                extract_folder = item.filename
                break
    for filename in os.listdir(os.path.join(extract_path, extract_folder)):
        source = os.path.join(extract_path, extract_folder, filename)
        dest = os.path.join(extract_path, filename)
        shutil.move(source, dest)
    os.rmdir(extract_folder)
    os.remove(file_path)


def clean_files(file_list: list, clean: bool, debug: bool):
    """Delete all files in the file_list. Used to perform cleaning if ghau.update.Update.clean is enabled."""
    if clean:
        for path in file_list:
            message("Removing path {}".format(path), debug)
            os.remove(path)
    elif not clean:
        pass


def load_whitelist(root: str, whitelist: list, debug: bool = False) -> list:
    """Filter directory based on given whitelist. Returns any files not listed in the whitelist. This function utilizes
    wcmatch."""
    file_filter = ""
    dir_filter = ""
    f, d = 0, 0
    for item in whitelist:
        for key in item:
            if item[key] is False:
                if f == 0:  # wcmatch requires no '|' on the first entry.
                    file_filter += "!"+key
                else:
                    file_filter += "|!"+key
                f += 1
            elif item[key] is True:
                if d == 0:
                    dir_filter += key
                else:
                    dir_filter += "|"+key
                d += 1
    message("file_filter: {}".format(file_filter), debug)
    message("dir_filter: {}".format(dir_filter), debug)
    message("Checking whitelisted files in directory: {}".format(root), debug)
    pl = wcmatch.WcMatch(root, file_filter, dir_filter, flags=wcmatch.RECURSIVE |
                         wcmatch.DIRPATHNAME | wcmatch.FILEPATHNAME | wcmatch.GLOBSTAR).match()
    return pl
