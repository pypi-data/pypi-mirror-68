#!/usr/bin/env python3

"""Main script of the program"""

import getpass
import json
import os
import logging

from flickr.constants import FLICKR_KEY_FILE_NAME
from flickr.parser import get_arguments
from flickr.flickr_api import FlickrApi
from flickr.mirroring_agent import FlickrUserPhotostreamMirroringAgent


def config_debug_level(
        console_debug_level,
        file_debug_level=logging.DEBUG):
    """
    Config the debug level of console log and file log

    Args:
        console_debug_level, file_debug_level (int): Respectively represent the
            debug level of the console log and the file log
    """
    # Config File Log
    logging.basicConfig(
        format="%(asctime)s %(name)-24s %(levelname)-8s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename="mirror_flickr.log",
        filemode="w",
        level=file_debug_level)

    # Config Console Log
    console_log = logging.StreamHandler()
    console_log.setLevel(console_debug_level)
    formatter = logging.Formatter("%(name)-24s %(levelname)-8s %(message)s")
    console_log.setFormatter(formatter)
    global logger
    logger = logging.getLogger("")
    logger.addHandler(console_log)


def get_consumer_key_and_secret(cache_path, is_save_api_keys):
    """
    Get the consumer key and consumer secret from cache file or from user.
    Validate the consumer key the user provide

    Args:
        cache_path (str): The absolute path to the cache directory

        is_save_api_keys (bool): Indicates whether the app should save the
            consumer key and consumer secret to the cache file

    Raise:
        ValueError: If the consumer_key provided by the user is not valid

    Returns:
        consumer_key, consumer_secret (str): Respectively represent the valid
            consumer key and consumer secret
    """
    cache_path = os.path.join(cache_path, FLICKR_KEY_FILE_NAME)

    try:
        with open(cache_path, "r") as cache_file:
            consumer = json.load(cache_file)
            consumer_key = consumer["consumer_key"]
            consumer_secret = consumer["consumer_secret"]

        logger.debug("Using cache keys")

    except (FileNotFoundError, KeyError):
        logger.debug("No cache keys Found")
        consumer_key = getpass.getpass(prompt="Enter your Flickr API key:")
        consumer_secret = getpass.getpass(prompt="Enter your Flickr API secret:")

        test_flickr_api = FlickrApi(consumer_key, consumer_secret)

        if not test_flickr_api.check_api_key():
            raise ValueError(f"Invalid consumer_key {consumer_key}")

        if is_save_api_keys:
            with open(os.open(cache_path, os.O_CREAT | os.O_WRONLY, 0o600), "w") as cache_file:
                json.dump(
                    {
                        "consumer_key": consumer_key,
                        "consumer_secret": consumer_secret
                    },
                    cache_file
                )

    return consumer_key, consumer_secret


def main():
    """Entry point"""
    # Parse argument
    args = get_arguments()

    # Create the cache directory if it hasn't existed
    cache_path = os.path.abspath(os.path.expanduser(args.cache_path))
    if not os.path.isdir(cache_path):
        os.makedirs(cache_path)

    # Config Debug Level
    config_debug_level(args.debug_level)

    try:
        # Get and validate consumer key and consumer secret
        consumer_key, consumer_secret = \
            get_consumer_key_and_secret(cache_path, args.save_api_keys)

        # Validate content fetching
        if args.image_only and args.info_only:
            raise ValueError(
                "Choose either --image-only or --info-only option. To fetch ",
                "both image and info don't specify any of above option")

        # Initialize the mirroring agent
        mirroring_agent = FlickrUserPhotostreamMirroringAgent(
            args.username,
            consumer_key,
            consumer_secret,
            cache_root_path_name=cache_path,
            cache_directory_depth=args.cache_directory_depth,
            image_only=args.image_only,
            info_only=args.info_only,
            info_level=args.info_level,
            caching_strategy=args.caching_strategy
        )

        # Run the mirroring agent
        mirroring_agent.run()

    except ValueError as e:
        logger.critical(str(e))


if __name__ == "__main__":
    main()
