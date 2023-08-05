
from typing import List
from floodgateio.types.rollout_entity import RolloutEntity
from floodgateio.evaluators.evaluator_helper import EvaluatorHelper


class RolloutEvaluator:

    @staticmethod
    def evaluate(key, user_id, rollouts, default_value): 
        # type: (str, str, List[RolloutEntity], str) -> str

        scale = EvaluatorHelper.get_scale(key, user_id)

        rollout_lower_limit = 0
        rollout_upper_limit = 0
        rollout_value = default_value

        for rollout in rollouts:
            rollout_upper_limit += rollout.percentage
            if rollout_lower_limit < scale <= rollout_upper_limit:
                rollout_value = rollout.value
                break
            rollout_lower_limit += rollout.percentage

        return rollout_value
