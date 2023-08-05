
from typing import List
import logging

from floodgateio.types.user import User
from floodgateio.types.feature_flag_entity import FeatureFlagEntity
from floodgateio.evaluators.evaluator_helper import EvaluatorHelper
from floodgateio.evaluators.rollout_evaluator import RolloutEvaluator
from floodgateio.consts import Consts

logger = logging.getLogger('floodgateio')


class TargetEvaluator:

    @staticmethod
    def evaluate(key, user, flag, default_value):
        # type: (str, User, FeatureFlagEntity, str) -> str

        evaluates = True
        valid = False

        for target in flag.targets:
            evaluates = True
            for rule in target.rules:
                user_attribute_value = user.get_attribute_value(rule.attribute)
                if user_attribute_value:
                    user_attribute_value = user_attribute_value.lower()
                else:
                    evaluates = False
                    continue

                valid = TargetEvaluator.compare_rule_values(rule, user_attribute_value)

                logger.debug("comparator: {0}, attribute: {1}, valid: {2}".format(rule.comparator, user_attribute_value, valid))
                evaluates = evaluates and valid
        
            if evaluates:
                if target.is_rollout:
                    return RolloutEvaluator.evaluate(key, user.user_id, target.rollouts, default_value)
                return target.value

        if flag.is_rollout:
            return RolloutEvaluator.evaluate(key, user.user_id, flag.rollouts, default_value)

        return default_value

    @staticmethod
    def compare_rule_values(rule, user_attribute_value):
        if rule.comparator == Consts.COMPARATOR_EQUAL_TO:
            valid = bool([v for v in rule.values if v.lower() == user_attribute_value])

        elif rule.comparator == Consts.COMPARATOR_NOT_EQUAL_TO:
            valid = not bool([v for v in rule.values if v.lower() == user_attribute_value])

        elif rule.comparator == Consts.COMPARATOR_GREATER:
            valid = float(user_attribute_value) > float(rule.values[0]) if rule.values else False

        elif rule.comparator == Consts.COMPARATOR_GREATER_EQUAL_TO:
            valid = float(user_attribute_value) >= float(rule.values[0]) if rule.values else False

        elif rule.comparator == Consts.COMPARATOR_LESS:
            valid = float(user_attribute_value) < float(rule.values[0]) if rule.values else False

        elif rule.comparator == Consts.COMPARATOR_LESS_EQUAL_TO:
            valid = float(user_attribute_value) <= float(rule.values[0]) if rule.values else False

        elif rule.comparator == Consts.COMPARATOR_CONTAINS:
            valid = bool([v for v in rule.values if v.lower() in user_attribute_value])

        elif rule.comparator == Consts.COMPARATOR_NOT_CONTAIN:
            valid = bool([v for v in rule.values if v.lower() not in user_attribute_value])

        elif rule.comparator == Consts.COMPARATOR_ENDS_WITH:
            valid = bool([v for v in rule.values if user_attribute_value.endswith(v.lower())])

        else:
            valid = False

        return valid
