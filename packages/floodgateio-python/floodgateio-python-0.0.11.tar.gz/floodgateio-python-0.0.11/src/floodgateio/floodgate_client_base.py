
from typing import Optional
import logging

from floodgateio.configurations.client_config_base import ClientConfigBase
from floodgateio.configurations.client_config_with_autoupdate import ClientConfigWithAutoUpdate
from floodgateio.types.user import User
from floodgateio.types.exceptions import FloodGateApiException
from floodgateio.types.feature_flag_entity import FeatureFlagEntity
from floodgateio.evaluators.rollout_evaluator import RolloutEvaluator
from floodgateio.evaluators.target_evaluator import TargetEvaluator
from floodgateio.utils.http_resource_fetcher import HttpResourceFetcher

logger = logging.getLogger('floodgateio')


class FloodGateClientBase:

    config = None  # type: ClientConfigBase

    def __init__(self, config):
        # type: (ClientConfigBase) -> None
        if not config.was_initialized:
            raise FloodGateApiException("Client config is not intialized."
                                        " Use FloodGateClient.initialize_* methods for proper initialization")

        self.config = config

    def get_value(self, key, default_value, override_user=None):
        # type: (str, str, Optional[User]) -> str
        flags = self.config.get_flags()

        user = self.config.get_user()
        if override_user:
            user = override_user

        if not flags:
            logger.error("No flag data available")
            return default_value

        flag = None  # type: Optional[FeatureFlagEntity]
        for f in flags:
            if f.key == key:
                flag = f
                break

        if not flag:
            logger.info("Flag {} not found".format(key))
            return default_value

        if not user:
            logger.info("Flag {0}: {1}".format(key, flag.value))
            return flag.value

        if not flag.is_targeting_enabled:
            if flag.is_rollout:
                return RolloutEvaluator.evaluate(key, user.user_id, flag.rollouts, flag.value)

        if flag.targets:
            return TargetEvaluator.evaluate(key, user, flag, flag.value)

        return default_value

    def __initialize_client(self):
        pass

    def __evaluate(self):
        pass
