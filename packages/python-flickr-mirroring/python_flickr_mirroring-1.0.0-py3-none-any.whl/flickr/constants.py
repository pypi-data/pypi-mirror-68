"""Constants of the package"""

from enum import Enum
from enum import auto

import logging
from uuid import UUID
from hashlib import md5

from urllib3 import Retry
from requests.adapters import HTTPAdapter


class CachingStrategy(Enum):
    """Represents the current use caching strategy"""
    LIFO = auto()
    FIFO = auto()


CONFIG_HTTP_REQUEST_RETRY = Retry(
    total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])

DEFAULT_ADAPTER = HTTPAdapter(max_retries=CONFIG_HTTP_REQUEST_RETRY)

FLICKR_PHOTO_NAMESPACE_UUID = UUID(hex=md5(b"FLICKR PHOTO").hexdigest())

HTTPS_SCHEME = "https://"

# End point to use flickr api
FLICKR_END_POINT = "https://www.flickr.com/services/rest/"

FLICKR_INVALID_API_KEY_ERROR_CODE = 100

FLICKR_KEY_FILE_NAME = "flickr_keys"

DEFAULT_PHOTOS_PER_PAGE = 100

FLICKR_PHOTO_IMAGE_EXTENSIONS = [".jpg", ".png", ".gif"]

JSON_EXTENSION = ".json"

MIRRORING_PROGRESS_FILE_NAME = "mirroring_progress.json"

DATE_FORMAT = "%b-%d-%Y %H:%M:%S"

# Debug level
DEBUG_LEVEL = (
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
)

# Mapping from ISO 639-1 alpha-2 code to ISO 639-3 alpha-3 code
LANGUAGE_CODE_MAPPING = {
    "aa": "aar", "ab": "abk", "af": "afr", "ak": "aka", "am": "amh",
    "ar": "ara", "an": "arg", "as": "asm", "av": "ava", "ae": "ave",
    "ay": "aym", "az": "aze", "ba": "bak", "bm": "bam", "be": "bel",
    "bn": "ben", "bh": "bih", "bi": "bis", "bo": "bod", "bs": "bos",
    "br": "bre", "bg": "bul", "ca": "cat", "cs": "ces", "ch": "cha",
    "ce": "che", "cu": "chu", "cv": "chv", "kw": "cor", "co": "cos",
    "cr": "cre", "cy": "cym", "da": "dan", "de": "deu", "dv": "div",
    "dz": "dzo", "el": "ell", "en": "eng", "eo": "epo", "et": "est",
    "eu": "eus", "ee": "ewe", "fo": "fao", "fa": "fas", "fj": "fij",
    "fl": "fil", "fi": "fin", "fr": "fra", "fy": "fry", "ff": "ful",
    "gd": "gla", "ga": "gle", "gl": "glg", "gv": "glv", "gn": "grn",
    "gu": "guj", "ht": "hat", "ha": "hau", "sh": "hbs", "he": "heb",
    "hz": "her", "hi": "hin", "ho": "hmo", "hr": "hrv", "hu": "hun",
    "hy": "hye", "ig": "ibo", "io": "ido", "ii": "iii", "iu": "iku",
    "ie": "ile", "ia": "ina", "id": "ind", "ik": "ipk", "is": "isl",
    "it": "ita", "jv": "jav", "ja": "jpn", "kl": "kal", "kn": "kan",
    "ks": "kas", "ka": "kat", "kr": "kau", "kk": "kaz", "km": "khm",
    "ki": "kik", "rw": "kin", "ky": "kir", "kv": "kom", "kg": "kon",
    "ko": "kor", "kj": "kua", "ku": "kur", "lo": "lao", "la": "lat",
    "lv": "lav", "li": "lim", "ln": "lin", "lt": "lit", "lb": "ltz",
    "lu": "lub", "lg": "lug", "mh": "mah", "ml": "mal", "mr": "mar",
    "mk": "mkd", "mg": "mlg", "mt": "mlt", "mn": "mon", "mi": "mri",
    "ms": "msa", "my": "mya", "na": "nau", "nv": "nav", "nr": "nbl",
    "nd": "nde", "ng": "ndo", "ne": "nep", "nl": "nld", "nn": "nno",
    "nb": "nob", "no": "nor", "ny": "nya", "oc": "oci", "oj": "oji",
    "or": "ori", "om": "orm", "os": "oss", "pa": "pan", "pi": "pli",
    "pl": "pol", "pt": "por", "ps": "pus", "qu": "que", "rm": "roh",
    "ro": "ron", "rn": "run", "ru": "rus", "sg": "sag", "sa": "san",
    "si": "sin", "sk": "slk", "sl": "slv", "se": "sme", "sm": "smo",
    "sn": "sna", "sd": "snd", "so": "som", "st": "sot", "es": "spa",
    "sq": "sqi", "sc": "srd", "sr": "srp", "ss": "ssw", "su": "sun",
    "sw": "swa", "sv": "swe", "ty": "tah", "ta": "tam", "tt": "tat",
    "te": "tel", "tg": "tgk", "tl": "tgl", "th": "tha", "ti": "tir",
    "to": "ton", "tn": "tsn", "ts": "tso", "tk": "tuk", "tr": "tur",
    "tw": "twi", "ug": "uig", "uk": "ukr", "ur": "urd", "uz": "uzb",
    "ve": "ven", "vi": "vie", "vo": "vol", "wa": "wln", "wo": "wol",
    "xh": "xho", "yi": "yid", "yo": "yor", "za": "zha", "zh": "zho",
    "zu": "zul"
}
