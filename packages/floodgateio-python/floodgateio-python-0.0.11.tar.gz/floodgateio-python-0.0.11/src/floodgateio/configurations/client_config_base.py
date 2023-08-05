

from typing import Optional, Any, List
import json
import logging
import codecs
from floodgateio.types.exceptions import FloodGateApiException
from floodgateio.types.feature_flag_entity import FeatureFlagEntity
from floodgateio.store.cache import Cache
from floodgateio.consts import Consts
from floodgateio.utils.converter import Converter
from floodgateio.utils.http_resource_fetcher import HttpResourceFetcher


logger = logging.getLogger('floodgateio')


class ClientConfigBase:

    API_VERSION = "v1"
    API_BASE_URL = "https://cdn.floodgate.io"

    sdk_key = None  # type: str
    user = None     # type: Optional[str]

    config_url = None   # type: str
    config_file = None  # type: str

    http_etag = None  # type: str

    __http_resource_fetcher = None  # type: HttpResourceFetcher
    __store = None  # type: Cache

    __was_initialized = False  # type: bool


    def __init__(self, sdk_key=None, config_url=None, config_file=None):
        self.sdk_key = sdk_key
        self.config_url = config_url
        self.config_file = config_file
        self.__store = Cache()

    http_resource_fetcher = property(lambda self: self.__http_resource_fetcher)
    was_initialized = property(lambda self: self.__was_initialized)

    def set_initialized(self):
        self.__was_initialized = True

    def validate_config(self):
        if not self.sdk_key:
            raise FloodGateApiException("SDK Key was empty")

    def update_store(self, key, data):
        logger.info("*** Config Cached (local) ***")
        self.__store.save(key, data)

    @staticmethod
    def validate_json(json_data):
        # type: (Any) -> bool
        if json_data and isinstance(json_data, list):
            return True
        return False

    def get_flags(self):
        json_data = self.__store.retreive(Consts.CACHE_NAME)
        return self.deserialize_conifg_json(json_data)

    def get_user(self):
        return self.user

    @staticmethod
    def deserialize_conifg_json(json_data):
        # type: (Any) -> List[FeatureFlagEntity]
        flags = []
        for f_json in json_data or []:
            f = FeatureFlagEntity()
            f.__setjson__(f_json)
            flags.append(f)
        return flags

    def build_url(self, endpoint):  # pylint: disable=unused-argument
        # type: (str) -> str
        base_url = self.config_url.rstrip("/") if self.config_url else self.API_BASE_URL
        return "{0}/environment-files/{1}/{2}/flags-config.json".format(base_url, self.sdk_key, self.API_VERSION)
