# -*- coding: utf-8 -*-

"""Represent The Flickr models"""

import logging
import os
import uuid

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

from flickr.constants import FLICKR_PHOTO_NAMESPACE_UUID
from flickr.constants import JSON_EXTENSION
from flickr.constants import LANGUAGE_CODE_MAPPING

logger = logging.getLogger(__name__)


class FlickrUser:
    """Represent a Flickr user"""

    def __init__(self, user_id, username):
        """Constructor of class Flickr User

        Args:
            user_id (str) -- Unique identification of a Flickr account
                (corresponding to the user's NSID)

            username (str) -- Username of this Flickr account.
        """
        if not isinstance(user_id, str) or not isinstance(username, str):
            raise TypeError("Args user_id and username MUST be string")
        self.__user_id = user_id
        self.__username = username

    @property
    def user_id(self):
        """str:The unique identification (NSID) of a Flickr account"""
        return self.__user_id

    @property
    def username(self):
        """str:The username of this Flickr account."""
        return self.__username

    @classmethod
    def from_json(cls, payload):
        """Return a FlickrUser object from the json payload

        Args:
            payload (dict) --  JSON expression correspond to the information of
                a particular username as returned by the Flickr API method
                flickr.people.findByUsername

                The payload has the following structure:
                    {
                        "id": string,
                        "nsid": string,
                        "username": {
                            "_content": string
                        }
                    }

        Raise:
            TypeError -- If the payload is not dictionary

        Return:
            (obj:`FlickrUser`) -- Represent a Flickr user
        """
        if not isinstance(payload, dict):
            raise TypeError("Argument payload MUST be JSON")

        try:
            user_id = payload["nsid"]
            username = payload["username"]["_content"]
        except KeyError as e:
            logger.error("Coudn't find %s", str(e))

        return cls(user_id, username)


class FlickrPhoto:
    """Represent a Flickr Photo"""

    def __init__(self, photo_id, title, upload_date):
        """Constructor of class Flickr Photo

        Args:
            photo_id (str) -- The photo identification

            title (str) -- The photo title

            upload_date(int) -- A UNIX timestamp represents the upload date of
                the photo
        """
        if not isinstance(photo_id, str) or not isinstance(title, str):
            raise TypeError("photo_id and title MUST be string")

        self.__photo_id = photo_id
        self.__photo_uuid = uuid.uuid5(FLICKR_PHOTO_NAMESPACE_UUID, photo_id)
        self.__title = self.__localized_text(title)

        self.__photo_sizes = None
        self.__description = None
        self.__comments = None
        self.__photo_info = {"title": self.__title.to_dict()}

        self.__upload_date = upload_date

    @property
    def id(self):
        """str:Represent the Flickr photo identification"""
        return self.__photo_id

    @property
    def file_name(self):
        """str:The unique file name without extension of the photo (A UUID in
        hex form)
        """
        return self.__photo_uuid.hex

    @property
    def image_filename(self):
        """str:The file name of the downloaded image of this photo"""
        if self.__photo_sizes is None:
            return None

        # The flickr url always surfix with a image extension (jpg|png|gif)
        # (https://www.flickr.com/services/api/misc.urls.html)
        image_file_extension = os.path.splitext(self.best_size.url)[-1]

        return f"{self.file_name}{image_file_extension}"

    @property
    def info_filename(self):
        """str:The file name to store the information of the photo"""
        return f"{self.file_name}{JSON_EXTENSION}"

    @property
    def title(self):
        """obj:`Label`:Represents the photo title"""
        return self.__title

    @property
    def sizes(self):
        """obj:`list` of obj:`FlickrPhotoSize`: All availabe size of the photo

        The setter method raise ValueError there is element of the proposed
        `sizes` is not a FlickrPhotoSize object.
        """
        return self.__photo_sizes

    @sizes.setter
    def sizes(self, sizes):
        for size in sizes:
            if not isinstance(size, FlickrPhotoSize):
                raise ValueError("All elements MUST be FlickrPhotoSize object")
        self.__photo_sizes = sizes

    @property
    def description(self):
        """obj:`Label`: Represent the description about the photo

        Setter method:
            Localize the proposed `description`(str), update the photo
            information

            Raise: TypeError if the `description` is not a string
        """
        return self.__description

    @description.setter
    def description(self, description):
        if not isinstance(description, str):
            raise TypeError("argument description MUST be string")

        self.__description = self.__localized_text(description)
        self.__photo_info["description"] = self.__description.to_dict()

    @property
    def comments(self):
        """obj:`list` of obj`Label`: Represent all the comments of the photo

        Setter method:
            Localize each comment of provided list of comments(`comments`),
            update the photo information

            Raise:
                TypeError: if the `comments` is not a list

                ValueError: if there is non-string element of `comments`
        """
        return self.__comments

    @comments.setter
    def comments(self, comments):
        if not isinstance(comments, list):
            raise TypeError("argument comments MUST be list")

        self.__photo_info["comments"] = []
        localized_comments = []
        for comment in comments:
            if not isinstance(comment, str):
                raise ValueError("comment content MUST be string")

            comment = self.__localized_text(comment)
            localized_comments.append(comment)
            self.__photo_info["comments"].append(comment.to_dict())

        self.__comments = localized_comments

    @property
    def best_size(self):
        """obj:`FlickrPhotoSize`:The largest size available of the photo"""
        if self.__photo_sizes is None:
            return None
        return max(self.__photo_sizes)

    @property
    def photo_info(self):
        """dict:Represent the information of the photo in JSON format"""
        return self.__photo_info

    @property
    def upload_date(self):
        """int:Represent the upload date of the photo in UNIX timestamp"""
        return self.__upload_date

    # Localized the provided `text` by try to detect text language, if fail
    # to detect the language use default language (English)
    @staticmethod
    def __localized_text(text):
        try:
            locale = detect(text)
        except (LangDetectException, ValueError) as e:
            logger.debug("Language detect: %s", str(e))
            return Label(text)

        locale = Locale.from_string(locale)
        return Label(text, locale=locale)

    @classmethod
    def from_json(cls, payload):
        """Return a FlickrPhoto object from the json payload

        Args:
            payload (dict) --  JSON expression correspond to the information of
                a particular username as returned by the Flickr API method
                flickr.people.getPhotos

                The payload has the following structure, Ex:
                    {
                        "id": "49510908217",
                        "owner": "13476480@N07",
                        "secret": "6f78f65cfd",
                        "server": "65535",
                        "farm": 66,
                        "title": "SAIGON 1974 - Rạch Bến Nghé, Bến Chương Dương",
                        "ispublic": 1,
                        "isfriend": 0,
                        "isfamily": 0,
                        "dateupload": 1588328621,
                    }

        Raise:
            TypeError -- If the payload is not dictionary

        Return:
            (obj:`FlickrPhoto`) -- Represent a Flickr photo
        """
        if not isinstance(payload, dict):
            raise TypeError("Argument payload MUST be JSON")

        try:
            photo_id = payload["id"]
            photo_title = payload["title"]
            photo_upload_date = int(payload["dateupload"])
        except KeyError as e:
            logger.error("Coudn't find %s", str(e))

        return cls(photo_id, photo_title, photo_upload_date)


class Locale:
    """Represent a tag respecting RFC 4646"""

    def __init__(self, language_code, country_code=""):
        """Constructor of Class Locale

        Args:
            language_code (str): An ISO 639-3 alpha-3 code (or alpha-2 code;
                which will be automatically converted to its equivalent ISO
                639-3 alpha-3 code).

            country_code (str, optional): An ISO 3166-1 alpha-2 code.
        """
        if (not isinstance(language_code, str)
                or not isinstance(country_code, str)):
            raise TypeError("language_code and country_code MUST be string")

        self.__language_code = self.normalize_language_code(language_code)
        self.__country_code = country_code

    def __repr__(self):
        """Formal String representation of `Locale` objects"""
        if self.__country_code:
            return f"{self.__language_code}-{self.__country_code}"
        return self.__language_code

    @staticmethod
    def normalize_language_code(language_code):
        """
        Check if the provided `languague_code` is an ISO 639-3 alpha-3 code (or
        alpha-2 code; which will be automatically converted to its equivalent
        ISO 639-3 alpha-3 code).

        Args:
            language_code (str): The proposed language code

        Raises:
            ValueError: If the `language_code` is not included in the
                LANGUAGE_CODE_MAPPING

        Returns:
            alpha_3_language_code (str): An ISO 639-3 alpha-3 code
        """
        num_of_language_code_characters = len(language_code)

        if num_of_language_code_characters == 2:
            alpha_3_language_code = LANGUAGE_CODE_MAPPING.get(language_code)
            if alpha_3_language_code is None:
                raise ValueError(f"{language_code} is not a valid language code")

        elif num_of_language_code_characters == 3:
            if language_code in LANGUAGE_CODE_MAPPING.values():
                alpha_3_language_code = language_code
            else:
                raise ValueError(f"{language_code} is not a valid language code")

        else:
            raise ValueError("Wrong language_code format")
        return alpha_3_language_code

    @classmethod
    def from_string(cls, locale):
        """Return a Locale object from the provided locale(str)

        Args:
            locale (str): A string representation of a locale, i.e., an ISO
                639-3 alpha-3 code (or alpha-2 code), optionally followed by a
                dash character - and an ISO 3166-1 alpha-2 code.

        Raise:
            TypeError -- If the argument `locale` is not a string

            ValueError -- If the `locale` is not a valid locale code

        Return:
            (obj:`Locale`) -- The locale object construct from provided `locale`
        """
        if not isinstance(locale, str):
            raise TypeError("argument locale MUST be a string")

        code = locale.split("-")
        num_of_components = len(code)
        if num_of_components not in (1, 2):
            raise ValueError("Wrong locale format")
        return cls(*code)


class Label:
    """
    Represents a humanly-readable textual content written in a given locale
    (English by default).
    """

    def __init__(self, content, locale=Locale("eng")):
        """Constructor of class Label

        Args:
            content (str): Humanly-readable textual content of the label.

            locale (obj:`Locale`, optional): Represents the language of the
                textual content of this label (English by default).
        """
        if not isinstance(content, str) or not isinstance(locale, Locale):
            raise TypeError("Wrong arguments type")

        self.__content = content
        self.__locale = locale

    @property
    def content(self):
        """str:Represent humanly-readable textual content of the label"""
        return self.__content

    @property
    def locale(self):
        """obj:`Locale`:The language of the textual content of this label"""
        return self.__locale

    def to_dict(self):
        """Return the dictionary representation of the object"""
        return {"content": self.content, "locale": str(self.locale)}


class FlickrPhotoSize:
    """Represent a valid size of Flickr Photo"""

    def __init__(self, label, width, height, url):
        """Constructor of class FlickrPhotoSize

        Args:
            label (str): The label representing the size of a photo.

            width, height (int): Respectively represents the width and height of
                the photo for this size in pixel

            url (str): The Uniform Resource Locator (URL) that references the
                image file of the photo for this size.
        """
        self.__label = label
        self.__width = width
        self.__height = height
        self.__url = url
        self.__size = width * height

    @property
    def label(self):
        """str:The label representing the size of a photo in textual form"""
        return self.__label

    @property
    def width(self):
        """int:The number of pixel columns of the photo for this size"""
        return self.__width

    @property
    def height(self):
        """int:The number of pixel rows of the photo for this size"""
        return self.__height

    @property
    def url(self):
        """
        str:The URL that references the image file of the photo for this size
        """
        return self.__url

    @property
    def size(self):
        """int:The total pixels of the photo for this size"""
        return self.__size

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.size == other.size

        raise TypeError(
            f"== not supported between instances of {self.__class__.__name__} "
            f"and '{other.__class__.__name__}'")

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.size < other.size
        return NotImplemented

    @classmethod
    def from_json(cls, payload):
        """Parse data from payload and create FlickrPhotoSizes object

        Args:
            payload (dict): JSON expression correspond to the information of
                a particular username as returned by the Flickr API method
                flickr.photos.getSizes

                {
                    "label": "Small 320",
                    "width": 320,
                    "height": 211,
                    "source": "https://live.staticflickr.com/...",
                    "url": "https://www.flickr.com/photos/...",
                    "media": "photo"
                }

        Raise:
            TypeError: If the payload is not dictionary

        Returns:
            (obj:`FlickrPhotoSize`): A valid size of Flickr Photo
        """
        if not isinstance(payload, dict):
            raise TypeError("Argument payload MUST be JSON")

        try:
            label = payload["label"]
            width = payload["width"]
            height = payload["height"]
            url = payload["source"]

        except KeyError as e:
            logger.error("Coudn't parse payload %s", str(e))

        return cls(label, width, height, url)
