
from typing import Optional
import logging
import asyncio

from floodgateio.configurations.client_config_async import ClientConfigAsync
from floodgateio.configurations.client_config_with_autoupdate_async import ClientConfigWithAutoUpdateAsync
from floodgateio.types.user import User
from floodgateio.types.exceptions import FloodGateApiException
from floodgateio.types.feature_flag_entity import FeatureFlagEntity
from floodgateio.evaluators.rollout_evaluator import RolloutEvaluator
from floodgateio.evaluators.target_evaluator import TargetEvaluator
from floodgateio.utils.http_resource_fetcher_aiohttp import HttpResourceFetcherAioHttp
from floodgateio.floodgate_client_base import FloodGateClientBase

logger = logging.getLogger('floodgateio')


class FloodGateClientAsync(FloodGateClientBase):

    @staticmethod
    def initialize_from_key(sdk_key):
        # type: (str) -> FloodGateClientAsync
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(FloodGateClientAsync.initialize_from_key_async(sdk_key))

    @staticmethod
    def initialize_from_config(config):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(FloodGateClientAsync.initialize_from_config_async(config))

    @staticmethod
    def initialize_from_key_autoupdate(sdk_key):
        # type: (str) -> FloodGateClientAsync
        config = ClientConfigWithAutoUpdateAsync(sdk_key)
        return FloodGateClientAsync.initialize_from_config(config)

    @staticmethod
    async def initialize_from_key_async(sdk_key):
        # type: (str) -> FloodGateClientAsync
        config = ClientConfigAsync(sdk_key)
        client = await FloodGateClientAsync.initialize_from_config_async(config)
        return client

    @staticmethod
    async def initialize_from_config_async(config):
        # type: (ClientConfigAsync) -> FloodGateClientAsync

        http = HttpResourceFetcherAioHttp()
        config.validate_config()
        await config.initialize_config_async(http)
        return FloodGateClientAsync(config)
