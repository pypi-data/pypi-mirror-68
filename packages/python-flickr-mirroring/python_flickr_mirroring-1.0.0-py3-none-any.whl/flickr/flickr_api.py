# -*- coding: utf-8 -*-

"""Module for class related to Flickr API"""

import logging
import requests

from flickr.constants import DEFAULT_ADAPTER
from flickr.constants import DEFAULT_PHOTOS_PER_PAGE
from flickr.constants import FLICKR_END_POINT
from flickr.constants import FLICKR_INVALID_API_KEY_ERROR_CODE
from flickr.constants import HTTPS_SCHEME

from flickr.flickr_model import FlickrUser
from flickr.flickr_model import FlickrPhoto
from flickr.flickr_model import FlickrPhotoSize

logger = logging.getLogger(__name__)


class FlickrApiError(Exception):
    """Raise when a Flickr API Error occured"""

    def __init__(self, code, message):
        """Constructor for class FlickrApiError

        Args:
            code (int): Represents the error code
            message (str): Represents the error message
        """
        if not isinstance(code, int) or not isinstance(message, str):
            raise TypeError("input wrong argument type")

        super().__init__(f"Code {code}: {message}")
        self.__code = code
        self.__message = message

    @property
    def code(self):
        """int:The error code"""
        return self.__code

    @property
    def message(self):
        """str:The error message"""
        return self.__message


class FlickrApi:
    """The RESTful API gateway to interact with Flickr"""

    def __init__(self, consumer_key, consumer_secret):
        """Construtor of the class FlickrApi

        Args:
            consumer_key, consumer_secret (str) -- The key and secret the
                consumer registers with Flickr to build app using their API
        """
        if (not isinstance(consumer_key, str)
                or not isinstance(consumer_secret, str)):
            raise TypeError("consumer_key and consumer_secret MUST be string")

        self.__key = consumer_key
        self.__secret = consumer_secret
        self.__session = requests.Session()
        self.__session.mount(HTTPS_SCHEME, DEFAULT_ADAPTER)

    # Call the flickr API with the provided `method`(str) and `args`(dict),
    # Return the payload if possible
    def __call_api(self, method, args=None):
        # Build the query params
        defaults_query_params = {
            "api_key": self.__key,
            "format": "json",
            "nojsoncallback": 1
        }

        defaults_query_params["method"] = method
        if args is not None:
            defaults_query_params.update(args)

        # Make a API call
        response = self.__session.get(
            FLICKR_END_POINT, params=defaults_query_params)

        # Check if the HTTP request was successful
        if response.status_code != 200:
            response.raise_for_status()

        # Decode from JSON string to JSON in form of dictionary
        try:
            payload = response.json()
        except ValueError:
            logger.error("Couldn't parse response: %s", str(payload.content))

        # Check if the Flickr API status was ok
        if payload["stat"] != "ok":
            raise FlickrApiError(payload["code"], payload["message"])

        return payload

    def close_request_session(self):
        """Close the request_session after done using the API"""
        self.__session.close()

    def check_api_key(self):
        """
        Check if the `consumer_key` provided by the user is valid. Return True
        if the key is valid, False otherwise.

        Returns:
            (bool): True if the consumer_key is valid, False otherwise
        """
        method = "flickr.test.echo"
        logger.info("Testing API key...")
        try:
            self.__call_api(method)
        except FlickrApiError as api_error:
            logger.error(str(api_error))
            if api_error.code == FLICKR_INVALID_API_KEY_ERROR_CODE:
                return False

        logger.info("API key valid")
        return True

    def find_user(self, username):
        """
        Send a request to Flickr API endpoint to fetch information about the
        specified `username` and return the `FlickrUser` object corresponding
        to the specified `username`

        Args:
            username (str) -- The Flickr user name we want to find

        Returns:
            user (obj:`FlickrUser`) -- Represent the infomation about the Flickr
                user with the specified `username`
        """
        if not isinstance(username, str):
            raise TypeError("username MUST be a string")

        method = "flickr.people.findByUsername"
        logger.debug("Calling %s('%s')", method, username)
        payload = self.__call_api(method, {"username": username})

        try:
            user = FlickrUser.from_json(payload["user"])
        except KeyError as e:
            logger.error("Couldn't parse user's info from payload %s", str(e))

        logger.info("Found user: %s - %s", user.username, user.user_id)
        return user

    def get_photos(
            self,
            user_id,
            page=1,
            per_page=DEFAULT_PHOTOS_PER_PAGE,
            min_upload_date=None,
            max_upload_date=None):
        """
        Send a request to Flickr API endpoint to fetch photos of the user
        specified by `user_id`

        Args:
            user_id (str): The NSID of a Flickr user

            page (int, optional): Representing the page of the user's
                photostream to return photos. Defaults to 1.

            per_page (int, optional): Representing the number of photos to
                return per page. Defaults to 100. Maximum allowed value is 500

            min_upload_date, max_upload_date (int): UNIX timestamps which
                respectively represents the minimum upload date of photo and
                the maximum upload date of photo that we want to fetch

        Returns a tuple of values:
            photos (obj:`list` of obj:`FlickrPhoto`): List of Photos of user
                specified by `user_id`.

            total_pages (int): The number of pages of per_page photos in the
                user's photostream.

            total_photos (int): The total number of photos in the user's
                photostream.
        """
        if (not isinstance(user_id, str)
                or not isinstance(page, int)
                or not isinstance(per_page, int)):
            raise TypeError("Wrong argument type")

        params = {
            "user_id": user_id,
            "page": page,
            "per_page": per_page,
            "extras": "date_upload"
        }
        if min_upload_date is not None:
            params["min_upload_date"] = min_upload_date
        if max_upload_date is not None:
            params["max_upload_date"] = max_upload_date

        method = "flickr.people.getPhotos"
        logger.debug("USER %s:%s", user_id, method)
        payload = self.__call_api(method, params)

        try:
            photos = []
            for photo in payload["photos"]["photo"]:
                photos.append(FlickrPhoto.from_json(photo))

            total_pages = int(payload["photos"]["pages"])
            total_photos = int(payload["photos"]["total"])

        except KeyError as e:
            logger.error("Couldn't parse user's photos from payload %s", str(e))

        # logger.info(
        #     "Fetching %d photos (page %d in %d pages, total %d photos)",
        #     per_page, page, total_pages, total_photos)

        logger.debug(
            "Photo List:\n%s",
            '\n'.join([f'- {photo.id}: ({photo.title.locale}) {photo.title.content}' for photo in photos])
        )

        return photos, total_pages, total_photos

    def get_photo_sizes(self, photo_id):
        """
        Send a request to Flickr API endpoint to fetch  all photo sizes of the
        photo specified by `photo_id`

        Args:
            photo_id (str): The identification of the Flickr photo

        Returns:
            photo_sizes (obj:`list` of obj:`FlickrPhotoSize`): All availabe
                sizes of the photo specified by the `photo_id`
        """
        if not isinstance(photo_id, str):
            raise TypeError("argument photo_id MUST string")

        params = {"photo_id": photo_id}

        method = "flickr.photos.getSizes"
        logger.debug("PHOTO %s:%s", photo_id, method)
        payload = self.__call_api(method, params)

        try:
            photo_sizes = []
            for photo_size in payload["sizes"]["size"]:
                photo_sizes.append(FlickrPhotoSize.from_json(photo_size))

        except KeyError as e:
            logger.error("Couldn't parse photo sizes from payload %s", str(e))

        # logger.info("Get %d different sizes", len(photo_sizes))

        logger.debug(
            "Sizes list:\n%s",
            '\n'.join([f'- {size.label}: {size.width}x{size.height} ({size.url})' for size in photo_sizes]))

        return photo_sizes

    def get_photo_description(self, photo_id):
        """
        Send a request to Flickr API endpoint to fetch the description of the
        photo specified by `photo_id`

        Args:
            photo_id (str): The identification of the Flickr photo to fetch
                description for

        Returns:
            description (str): The description of the photo specified by the
                `photo_id`
        """
        if not isinstance(photo_id, str):
            raise TypeError("argument photo_id MUST string")

        params = {"photo_id": photo_id}

        method = "flickr.photos.getInfo"
        logger.debug("PHOTO %s:%s", photo_id, method)
        payload = self.__call_api(method, params)

        try:
            description = payload["photo"]["description"]["_content"]
        except KeyError as e:
            logger.error("Couldn't parse description from payload %s", str(e))

        return description

    def get_photo_comments(self, photo_id):
        """
        Send a request to Flickr API endpoint to fetch all the comments of the
        photo specified by `photo_id`

        Args:
            photo_id (str): The identification of the Flickr photo to fetch
                comments for

        Returns:
            comments (obj:`list` of obj:`str`): All the comments of the photo
                specified by the `photo_id`
        """
        if not isinstance(photo_id, str):
            raise TypeError("argument photo_id MUST string")

        params = {"photo_id": photo_id}

        method = "flickr.photos.comments.getList"
        logger.debug("PHOTO %s:%s", photo_id, method)
        payload = self.__call_api(method, params)

        try:
            payload = payload["comments"]
        except KeyError as e:
            logger.error("Couldn't parse comments from payload %s", str(e))

        comment_contents = []
        try:
            comments = payload["comment"]
            for comment in comments:
                comment_contents.append(comment["_content"])
        except KeyError:
            logger.debug("Photo %s hasn't had any comment", photo_id)

        return comment_contents
