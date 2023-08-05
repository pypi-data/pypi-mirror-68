
from typing import Optional
import logging

from floodgateio.configurations.client_config_sync import ClientConfigSync
from floodgateio.configurations.client_config_with_autoupdate import ClientConfigWithAutoUpdate
from floodgateio.types.user import User
from floodgateio.types.exceptions import FloodGateApiException
from floodgateio.types.feature_flag_entity import FeatureFlagEntity
from floodgateio.evaluators.rollout_evaluator import RolloutEvaluator
from floodgateio.evaluators.target_evaluator import TargetEvaluator
from floodgateio.utils.http_resource_fetcher_requests import HttpResourceFetcherRequests
from floodgateio.floodgate_client_base import FloodGateClientBase

logger = logging.getLogger('floodgateio')


class FloodGateClient(FloodGateClientBase):

    @staticmethod
    def initialize_from_key(sdk_key):
        # type: (str) -> FloodGateClient
        config = ClientConfigSync(sdk_key)
        return FloodGateClient.initialize_from_config(config)

    @staticmethod
    def initialize_from_key_autoupdate(sdk_key):
        # type: (str) -> FloodGateClient
        config = ClientConfigWithAutoUpdate(sdk_key)
        return FloodGateClient.initialize_from_config(config)

    @staticmethod
    def initialize_from_config(config):
        # type: (ClientConfigSync) -> FloodGateClient
        http = HttpResourceFetcherRequests()
        config.validate_config()
        config.initialize_config(http)
        return FloodGateClient(config)
