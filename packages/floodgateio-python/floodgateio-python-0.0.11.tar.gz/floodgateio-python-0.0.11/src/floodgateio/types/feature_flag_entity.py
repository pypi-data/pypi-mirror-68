
from typing import List
from floodgateio.types.rollout_entity import RolloutEntity
from floodgateio.types.target_entity import TargetEntity
from floodgateio.utils.converter import Converter


class FeatureFlagEntity:

    key = None  # type: str
    value = None  # type: str
    is_rollout = None  # type: bool
    rollouts = None  # type: List[RolloutEntity]
    is_targeting_enabled = None  # type: bool
    targets = None  # type: List[TargetEntity]

    def __init__(self):
        self.rollouts = []

    def __setjson__(self, dct):
        self.key = dct['key']

        self.value = Converter.parse_bool_or_value(dct['value'])
        self.is_rollout = Converter.parse_bool(dct['is_rollout'])
        self.rollouts = Converter.decode_json_list_of_class(dct.get('rollouts'), RolloutEntity)

        self.is_targeting_enabled = Converter.parse_bool(dct['is_targeting_enabled'])
        self.targets = Converter.decode_json_list_of_class(dct.get('targets'), TargetEntity)
