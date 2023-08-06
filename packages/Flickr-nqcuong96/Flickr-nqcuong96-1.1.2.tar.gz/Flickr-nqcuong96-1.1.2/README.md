# Flickr Mirroring
* This project develops a command-line tool to mirror Flickr photo.
## Requirements
*  [Python 3.7](https://www.python.org/)
*  [langdetect](https://pypi.org/project/langdetect/)
*  [iso-639](https://pypi.org/project/iso-639/)
*  [iso3166](https://pypi.org/project/iso3166/)
*  [requests](https://pypi.org/project/requests/)
## Installation
- Install from PyPI database:

```bash
# Setup a binary directory to install our Flickr mirroring utility
$ mkdir -p ~/.local/bin/intek_flickr_mirroring
$ cd ~/.local/bin/intek_flickr_mirroring

# Setup a Python virtual environment
$ pipenv shell --three
Creating a virtualenv for this project...
Pipfile: /home/intek/.local/bin/intek_flickr_mirroring/Pipfile
Using /usr/local/bin/python3.7 (3.7.4) to create virtualenv...
⠦ Creating virtual environment...Using base prefix '/usr/local'
New python executable in /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0/bin/python3.7
Also creating executable in /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0/bin/python
Installing setuptools, pip, wheel...done.
Running virtualenv with interpreter /usr/local/bin/python3.7

✔ Successfully created virtual environment!
Virtualenv location: /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0
Creating a Pipfile for this project...
Launching subshell in virtual environment...
 . /home/intek/.virtualenvs/intek_flickr_mirroring-wqvphFZ0/bin/activate

# Install our Flickr mirroring utility
(intek_flickr_mirroring) $ pipenv install Flickr-nqcuong96
Installing Flickr-nqcuong96...
Adding Flickr-nqcuong96 to Pipfile's [packages]...
✔ Installation Succeeded
Pipfile.lock not found, creating...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
✔ Success!
Updated Pipfile.lock (96799b)!
Installing dependencies from Pipfile.lock (96799b)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 38/38 — 00:00:56
```

## Usage
* Using Flickr Mirroring to like other CLI tools:
```bash
# Execute our Bash script
(intek_flickr_mirroring) $ mirror_flickr --help
usage: __main__.py [-h] --username USERNAME [--cache-path CACHE_PATH]
                   [--consumer-key CONSUMER_KEY]
                   [--consumer-secret CONSUMER_SECRET] [--save-api-keys]
                   [--image-only] [--info-only] [--info-level {0,1,2}]
                   [--fifo] [--lifo]

This script support several features such as, to allow our users to mirror
images only, information (i.e.,title, description, comments) only, or both.

optional arguments:
  -h, --help            show this help message and exit

  --username USERNAME   username of the account of a user on Flickr to mirror
                        their photostream

  --cache-path CACHE_PATH
                        specify the absolute path where the photos downloaded
                        from Flickr need to be cached

  --consumer-key CONSUMER_KEY
                        a unique string used by the Consumer to identify
                        themselves to the Flickr API

  --consumer-secret CONSUMER_SECRET
                        a secret used by the Consumer to establish ownership
                        of the Consumer Key

  --save-api-keys       specify whether to save the Flickr API keys for
                        further usage

  --image-only          specify whether the script must only download
                        photos'images

  --info-only           specify whether the script must only download
                        photos'information

  --info-level {0,1,2}  specify the level of information of a photo to fetch
                        (value between 0 and 2)

  --fifo                specify the First-In First-Out method to mirror the
                        user's photostream, from the oldest uploaded photo to
                        the earliest

  --lifo                specify the Last-In First-Out method to mirror the
                        user's photostream, from the earliest uploaded photo
                        to the oldest (default option)
```
