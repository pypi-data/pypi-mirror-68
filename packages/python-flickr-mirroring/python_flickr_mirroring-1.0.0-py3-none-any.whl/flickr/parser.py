"""Command Line Interface for mirroring Flickr"""

import argparse
import logging
from flickr.constants import DEBUG_LEVEL

from flickr.constants import CachingStrategy

class SetLoggingLevel(argparse.Action):
    """Set the logging level according to user input argument"""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, DEBUG_LEVEL[values])


def get_arguments():
    """
    Parse the arguments out of the command line. Convert arguments string to
    objects and assign them as attributes of the namespace.

    Return: an instance `argparse.Namespace` corresponding to the current
        namespace.
    """
    # Creating an ArgumentParser object
    parser = argparse.ArgumentParser(
        prog="mirror_flickr", description="Flickr Mirroring.")

    # Adding argument
    parser.add_argument(
        "--username", required=True,
        help="username of the account of a user on Flickr to mirror their \
            photostream"
    )

    parser.add_argument(
        "--cache-path", default="~/.flickr/",
        help="The absolute path where the script saves photos downloaded from \
            Flickr."
    )

    parser.add_argument(
        "--cache-directory-depth", type=int, default=4,
        help="The depth of the directory structure")

    parser.add_argument(
        "--save-api-keys", action="store_true",
        help="Specify whether to save the Flickr API keys for further usage"
    )

    photo_data_group = parser.add_mutually_exclusive_group()

    photo_data_group.add_argument(
        "--image-only", action="store_true",
        help="Specify whether the script must only download photo's images"
    )

    photo_data_group.add_argument(
        "--info-only", action="store_true",
        help="Specify whether the script must only download photo's information"
    )

    parser.add_argument(
        "--info-level", metavar="LEVEL", type=int, choices=range(3), default=0,
        help="specify the level of information of a photo to fetch (value \
            between 0 and 2)"
    )

    parser.add_argument(
        "--debug", dest="debug_level", metavar="LEVEL", type=int,
        choices=range(5), default=logging.CRITICAL, action=SetLoggingLevel,
        help="specify the logging level (value between 0 and 4, from critical \
            to debug)"
    )

    parser.set_defaults(caching_strategy=CachingStrategy.LIFO)

    caching_strategy_group = parser.add_mutually_exclusive_group()

    caching_strategy_group.add_argument(
        "--fifo", dest="caching_strategy", action="store_const",
        const=CachingStrategy.FIFO,
        help="specify the First-In First-Out method to mirror the user's \
            photostream, from the oldest uploaded photo to the earliest"
    )

    caching_strategy_group.add_argument(
        "--lifo", dest="caching_strategy", action="store_const",
        const=CachingStrategy.LIFO,
        help="specify the Last-In First-Out method to mirror the user's \
            photostream, from the earliest uploaded photo"
    )

    return parser.parse_args()
