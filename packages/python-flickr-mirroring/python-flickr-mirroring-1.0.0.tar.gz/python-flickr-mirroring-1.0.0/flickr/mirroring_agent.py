# -*- coding: utf-8 -*-

"""Class related to the mirroring agent of specific Flickr user photostream"""

from datetime import datetime
import json
import logging
import os
import queue

import requests
from sympy import Interval
from sympy import Union
from sympy import Complement

from flickr.constants import CachingStrategy
from flickr.constants import DATE_FORMAT
from flickr.constants import DEFAULT_ADAPTER
from flickr.constants import FLICKR_PHOTO_IMAGE_EXTENSIONS
from flickr.constants import HTTPS_SCHEME
from flickr.constants import JSON_EXTENSION
from flickr.constants import MIRRORING_PROGRESS_FILE_NAME

from flickr.flickr_api import FlickrApi

logger = logging.getLogger(__name__)


class FlickrUserPhotostreamMirroringAgent:
    """Represent the User Photostream Mirroring Agent"""

    def __init__(
            self,
            username,
            flickr_consumer_key,
            flickr_consumer_secret,
            cache_root_path_name=None,
            cache_directory_depth=4,
            image_only=False,
            info_only=False,
            info_level=0,
            caching_strategy=CachingStrategy.LIFO):
        """Constructor for class FlickrUserPhotostreamMirroringAgent

        Args:
            username (str): Username of the account of a user on Flickr to
                mirror their photostream.

            flickr_consumer_key (str):  A unique string used by the Consumer to
                identify themselves to the Flickr API.

            flickr_consumer_secret (str): A secret used by the Consumer to
                establish ownership of the Consumer Key.

            cache_root_path_name (str, optional): Specify the absolute path
                where the images and/or information of the photos downloaded
                from Flickr need to be stored. (Defaults to None)

            cache_directory_depth (int, optional):  Number of sub-directories
                the cache file system is composed of. (Defaults to 4)

            image_only (bool, optional): Specify whether the script must only
                download photo's images. (Defaults to False)

            info_only (bool, optional):  Specify whether the agent must only
                download photos' information. (Defaults to False)

            info_level (int, optional): Specify the level of information of a
                photo to fetch (value between 0 and 2)

            caching_strategy (obj:`CachingStrategy`): Indicate whether the
                script using LIFO or FIFO strategy to cache photo
        """
        self.__session = None

        self.__flickr_api = FlickrApi(flickr_consumer_key, flickr_consumer_secret)
        self.__flickr_user = self.__flickr_api.find_user(username)

        self.__cache_root_path_name = cache_root_path_name
        self.__cache_user_path_name = os.path.join(cache_root_path_name, username)
        self.__cache_directory_depth = cache_directory_depth

        self.__info_level = info_level

        self.__is_fetching_image = not info_only
        self.__is_fetching_info = not image_only

        self.__caching_strategy = caching_strategy

        self.__newest_upload_date = self.__get_newest_photo_upload_date()
        self.__current_upload_date = None

        self.__progress_file_path = os.path.join(
            self.__cache_user_path_name, MIRRORING_PROGRESS_FILE_NAME)

        self.__last_progress = None

    @property
    def user(self):
        """
        obj:`FlickrUser`:Representing the user whose photostream is going to be
        mirrored by the instance of the class
        """
        return self.__flickr_user

    # Generate the absolute filepath name of the file in the deep directory
    # structure
    def __generate_file_path_name(self, filename):
        directories = [filename[i] for i in range(self.__cache_directory_depth)]
        return os.path.join(self.__cache_user_path_name, *directories, filename)

    # Get the newest photo upload date (A UNIX timestamp)
    def __get_newest_photo_upload_date(self):
        first_photo, _, _ = self.__flickr_api.get_photos(
            self.user.user_id, page=1, per_page=1
        )
        return first_photo[0].upload_date

    # Get all intervals of photos (separate by upload date) that haven't been
    # cached
    def __get_intervals_to_mirror(self):
        if not os.path.isfile(self.__progress_file_path):
            return None

        with open(self.__progress_file_path, "r") as image_progress_file:
            last_progess = json.load(image_progress_file)

        last_progess = [Interval(*sorted(interval)) for interval in last_progess]
        self.__last_progress = Union(*last_progess)

        intervals = Complement(
            Interval(0, self.__newest_upload_date), self.__last_progress)

        return intervals

    # Download the photo image of the specified `photo`(obj:`FlickrPhoto`)
    def __download_photo_image(self, photo):
        photo_sizes = self.__flickr_api.get_photo_sizes(photo.id)
        photo.sizes = photo_sizes

        response = self.__session.get(photo.best_size.url)
        if response.status_code != 200:
            response.raise_for_status()

        image_file_path_name = \
            self.__generate_file_path_name(photo.image_filename)

        # Create intermediate directories that contain the file
        dir_path = os.path.dirname(image_file_path_name)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        with open(image_file_path_name, "wb") as image_file:
            image_file.write(response.content)

        # logger.info("Save photo %s at %s", photo.id, image_file_path_name)
        logger.info("Caching image of photo %s", photo.image_filename)

    # Caching the photo information of specified `photo`(obj:`FlickrPhoto`) into
    # json file
    def __caching_photo_information(self, photo):
        # Update photo information
        if self.__info_level >= 1:
            description = self.__flickr_api.get_photo_description(photo.id)
            photo.description = description
        if self.__info_level == 2:
            comments = self.__flickr_api.get_photo_comments(photo.id)
            photo.comments = comments

        # Generate photo info file path name
        information_file_path_name = \
            self.__generate_file_path_name(photo.info_filename)

        # Create intermediate directories that contain the file
        dir_path = os.path.dirname(information_file_path_name)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        with open(information_file_path_name, "w", encoding="utf-8") as json_file:
            json.dump(photo.photo_info, json_file, ensure_ascii=False, indent=4)

        logger.info("Caching information of photo %s", photo.info_filename)

    # Starting new request session and set up page queue according to caching
    # strategy
    def __start_up(self):
        self.__session = requests.Session()
        self.__session.mount(HTTPS_SCHEME, DEFAULT_ADAPTER)

        logger.info(
            "Start mirroring photostream of %s(NSID=%s)",
            self.user.username,
            self.user.user_id)

    # Clean up the request session
    def __tear_down(self):
        self.__session.close()
        self.__flickr_api.close_request_session()
        logger.info("Closing request session")
        self.__log_progress_to_file()

    # Log mirroring progress to JSON file for resuming purpose
    def __log_progress_to_file(self):
        # Get the current mirroring progress
        if self.__caching_strategy is CachingStrategy.LIFO:
            progress = \
                Interval(self.__current_upload_date, self.__newest_upload_date)
        else:
            progress = Interval(0, self.__current_upload_date)

        # Merge current progress with last progress
        if self.__last_progress is not None:
            progress = Union(self.__last_progress, progress)

        # Format the progress to log to json file
        current_progress = []
        if isinstance(progress, Interval):
            current_progress.append([int(progress.left), int(progress.end)])
        else:
            for interval in progress.args:
                current_progress.append([int(interval.left), int(interval.end)])

        with open(self.__progress_file_path, "w") as progress_file:
            json.dump(current_progress, progress_file, indent=4)

        logger.info("Log progress to file")

    # Mirroring Flickr Photo of User in a specific period of time - specified by
    # `min_upload_date` and `max_upload_date`
    #
    # Args:
    #   min_upload_date, max_upload_date (int): An UNIX timestamp represent the
    #       minimum and maximum upload date to mirror photo respectively
    def __mirroring(self, min_upload_date=None, max_upload_date=None):
        min_upload_date = min_upload_date if min_upload_date else None

        # Format time stamp
        if max_upload_date:
            end_date = \
                datetime.utcfromtimestamp(max_upload_date).strftime(DATE_FORMAT)
        else:
            end_date = "Lastest photo"

        if min_upload_date:
            start_date = \
                datetime.utcfromtimestamp(min_upload_date).strftime(DATE_FORMAT)
        else:
            start_date = "Oldest photo"

        logger.info("Scanning image from %s to %s", start_date, end_date)

        # Create pages queue according to caching strategy
        _, total_pages, _ = \
            self.__flickr_api.get_photos(
                self.user.user_id,
                min_upload_date=min_upload_date,
                max_upload_date=max_upload_date
            )

        if self.__caching_strategy is CachingStrategy.LIFO:
            pages_queue = queue.Queue()
        else:
            pages_queue = queue.LifoQueue()

        for page in range(1, total_pages + 1):
            pages_queue.put(page)

        while not pages_queue.empty():
            # Get next page
            page = pages_queue.get()
            # Get photos list of the page
            photos, _, _ = \
                self.__flickr_api.get_photos(
                    self.user.user_id,
                    page=page,
                    min_upload_date=min_upload_date,
                    max_upload_date=max_upload_date
                )

            logger.info("Scanning page %d/%d...", page, total_pages)

            # Create photos queue according to caching strategy
            if self.__caching_strategy is CachingStrategy.LIFO:
                photos_queue = queue.Queue()
            else:
                photos_queue = queue.LifoQueue()

            for photo in photos:
                photos_queue.put(photo)

            # Download all the photos that hasn't been cached of the page
            while not photos_queue.empty():
                # Get next Photo
                photo = photos_queue.get()

                # The file path name of the photo without extension
                photo_file_path_name = \
                    self.__generate_file_path_name(photo.file_name)

                if self.__is_fetching_image:
                    # Download the photo image if it hasn't been cached
                    for extension in FLICKR_PHOTO_IMAGE_EXTENSIONS:
                        image_file_path_name = f"{photo_file_path_name}{extension}"
                        if os.path.isfile(image_file_path_name):
                            logger.info("CACHE HIT %s", image_file_path_name)
                            break
                    else:
                        self.__download_photo_image(photo)

                if self.__is_fetching_info:
                    info_file_path_name = f"{photo_file_path_name}{JSON_EXTENSION}"
                    # Get the photo information if it hasn't been cached
                    if os.path.isfile(info_file_path_name):
                        logger.info("CACHE HIT %s", info_file_path_name)
                    else:
                        self.__caching_photo_information(photo)

                self.__current_upload_date = photo.upload_date

    def run(self):
        """Start mirroring the user's photostream"""
        self.__start_up()

        try:
            intervals = self.__get_intervals_to_mirror()
            if intervals is None:
                # First run
                self.__mirroring()
            elif isinstance(intervals, Interval):
                # Only one interval to mirror
                self.__mirroring(
                    min_upload_date=intervals.left,
                    max_upload_date=intervals.end)
            else:
                # Multiple intervals to mirror
                if self.__caching_strategy is CachingStrategy.LIFO:
                    interval_queue = queue.LifoQueue()
                else:
                    interval_queue = queue.Queue()

                for interval in intervals.args:
                    interval_queue.put(interval)

                while not interval_queue.empty():
                    interval = interval_queue.get()
                    self.__mirroring(
                        min_upload_date=interval.left,
                        max_upload_date=interval.end)

        except Exception as e:
            logger.error(str(e))
        finally:
            self.__tear_down()
