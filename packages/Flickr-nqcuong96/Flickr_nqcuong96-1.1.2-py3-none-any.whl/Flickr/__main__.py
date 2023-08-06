#!/usr/bin/env python3

import argparse
import getpass

from Flickr.model.flickr import *


def get_arguments():
    parser = argparse.ArgumentParser(
        description="This script support several features such as, to allow our users to mirror images only, information (i.e.,title, description, comments) only, or both.")

    parser.add_argument("--username", action="store", type=str, required=True,
                        help="username of the account of a user on Flickr to mirror their photostream")
    parser.add_argument("--cache-path",  action="store", type=str, default="~/.flickr/",
                        help="specify the absolute path where the photos downloaded from Flickr need to be cached")
    parser.add_argument("--consumer-key", action="store", type=str,
                        help="a unique string used by the Consumer to identify themselves to the Flickr API")
    parser.add_argument("--consumer-secret", action="store", type=str,
                        help="a secret used by the Consumer to establish ownership of the Consumer Key")
    parser.add_argument("--save-api-keys", action="store_true", default=False,
                        help="specify whether to save the Flickr API keys for further usage")
    parser.add_argument("--image-only", action="store_true", default=False,
                        help="specify whether the script must only download photos'images")
    parser.add_argument("--info-only", action="store_true", default=False,
                        help="specify whether the script must only download photos'information")
    parser.add_argument("--info-level", action="store", type=int, choices=range(0, 3),
                        default=0, help="specify the level of information of a photo to fetch (value between 0 and 2)")
    parser.add_argument("--fifo", action="store_true", default=False,
                        help="specify the First-In First-Out method to mirror the user's photostream, from the oldest uploaded photo to the earliest")
    parser.add_argument("--lifo", action="store_false", default=True,
                        help="specify the Last-In First-Out method to mirror the user's photostream, from the earliest uploaded photo to the oldest (default option)")

    return parser.parse_args()


def main():
    args = get_arguments()

    if args.image_only and args.info_only:
        raise Exception("'image_only and info_only only choose once")

    if not args.lifo and args.fifo:
        raise Exception("'fifo' or 'lifo' only choose once")

    if args.fifo:
        caching_strategy = CachingStrategy.FIFO
    else:
        caching_strategy = CachingStrategy.LIFO

    if args.cache_path[-1] != "/":
        path = os.path.abspath(os.path.expanduser(
            args.cache_path) + "/flickr_keys")
    else:
        path = os.path.abspath(os.path.expanduser(
            args.cache_path) + "flickr_keys")

    key = None
    secrect = None

    if args.save_api_keys:
        key = getpass.getpass("Enter your Flickr API key: ")
        secrect = getpass.getpass("Enter your Flickr API secret: ")

        data = {
            "consumer_key": key,
            "consumer_secret": secrect,
        }

        try:
            with open(path, "w+") as outfile:
                json.dump(data, outfile)
        except FileNotFoundError:
            os.mkdir(os.path.abspath(os.path.expanduser(args.cache_path)))
            with open(path, "w+") as outfile:
                json.dump(data, outfile)
    else:
        if os.path.isfile(path):
            with open(path) as json_file:
                data = json.load(json_file)
                try:
                    key = data["consumer_key"]
                    secrect = data["consumer_secret"]
                except:
                    pass

        if key:
            print("Check API KEY      ")
            link = TEST_LINK.format(key)
            r = requests.get(url=link)
            data = r.json()
            r.close()

            if data["stat"] == "fail":
                print("WRONG API KEY! PLEASE INPUT NEW KEY")
                key = None

        if not key:
            key = getpass.getpass("Enter your Flickr API key: ")
            secrect = getpass.getpass("Enter your Flickr API secret: ")

    KEY = key
    SECRECT = secrect

    mirroring_agent = FlickrUserPhotostreamMirroringAgent(
        args.username, KEY, SECRECT, cache_root_path_name=args.cache_path, cache_directory_depth=4,
        image_only=args.image_only, info_level=args.info_level, info_only=args.info_only, caching_strategy=caching_strategy)

    mirroring_agent.run()


if __name__ == "__main__":
    main()
    # ./flickr.py --username manhhai --cache-path "./.flickr/" --image-only
