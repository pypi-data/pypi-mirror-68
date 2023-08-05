
from typing import Optional, Any, List
import json
import logging
import codecs
import asyncio

from floodgateio.types.exceptions import FloodGateApiException
from floodgateio.types.feature_flag_entity import FeatureFlagEntity
from floodgateio.store.cache import Cache
from floodgateio.consts import Consts
from floodgateio.utils.converter import Converter
from floodgateio.utils.http_resource_fetcher_aiohttp import HttpResourceFetcherAioHttp
from floodgateio.configurations.client_config_base import ClientConfigBase


logger = logging.getLogger('floodgateio')


class ClientConfigAsync(ClientConfigBase):

    async def initialize_config_async(self, http_resource_fetcher):
        # type: (HttpResourceFetcherAioHttp) -> None
        self.__http_resource_fetcher = http_resource_fetcher
        await self.load_data_async()
        self.set_initialized()

    async def load_data_async(self):
        try:
            if self.config_file:
                await self.fetch_flags_locally_async()
            await self.fetch_flags_server_async()
        except (KeyboardInterrupt, SystemExit):  # pylint: disable=try-except-raise
            raise
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Faild to load data [{0}] {1}".format(e.__class__.__name__, e))

    async def fetch_flags_locally_async(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.__fetch_flags_locally)
        
    def __fetch_flags_locally(self):
        logger.info("Loading flag data from local file: {}".format(self.config_file))
        data = open(self.config_file, 'r').read()
        data = codecs.decode(data.encode(), 'utf-8-sig')
        json_data = json.loads(data) or {}
        if self.validate_json(json_data):
            self.update_store(Consts.CACHE_NAME, json_data)

    async def fetch_flags_server_async(self):
        logger.info("Requesting flag data from server")
        url = self.build_url("flags")
        data, etag = await self.__http_resource_fetcher.fetch_async(url, self.sdk_key, self.http_etag)
        json_data = json.loads(data) if data else {}
        if self.validate_json(json_data):
            self.update_store(Consts.CACHE_NAME, json_data)
            self.http_etag = etag
