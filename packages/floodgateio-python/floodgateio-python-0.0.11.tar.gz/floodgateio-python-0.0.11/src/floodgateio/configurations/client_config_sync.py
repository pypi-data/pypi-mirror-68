

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
from floodgateio.configurations.client_config_base import ClientConfigBase


logger = logging.getLogger('floodgateio')


class ClientConfigSync(ClientConfigBase):

    def initialize_config(self, http_resource_fetcher):
        # type: (HttpResourceFetcher) -> None
        self.__http_resource_fetcher = http_resource_fetcher
        self.load_data()
        self.set_initialized()

    def load_data(self):
        try:
            if self.config_file:
                self.fetch_flags_locally()
            self.fetch_flags_server()
        except (KeyboardInterrupt, SystemExit):  # pylint: disable=try-except-raise
            raise
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Faild to load data [{0}] {1}".format(e.__class__.__name__, e))

    def fetch_flags_locally(self):
        logger.info("Loading flag data from local file: {}".format(self.config_file))

        data = open(self.config_file, 'r').read()
        data = codecs.decode(data.encode(), 'utf-8-sig')
        json_data = json.loads(data) or {}
        if self.validate_json(json_data):
            self.update_store(Consts.CACHE_NAME, json_data)

    def fetch_flags_server(self):
        logger.info("Requesting flag data from server")

        url = self.build_url("flags")
        data, etag = self.__http_resource_fetcher.fetch(url, self.sdk_key, self.http_etag)
        json_data = json.loads(data) if data else {}
        if self.validate_json(json_data):
            self.update_store(Consts.CACHE_NAME, json_data)
            self.http_etag = etag
