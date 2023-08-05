from typing import List
from floodgateio.types.rollout_entity import RolloutEntity
from floodgateio.types.rule_entity import RuleEntity
from floodgateio.utils.converter import Converter


class TargetEntity:

    target_id = None   # type: str
    state = None       # type: bool
    value = None       # type: str
    is_rollout = None  # type: bool
    rollouts = None    # type: List[RolloutEntity]
    rules = None       # type: List[RuleEntity]

    def __init__(self):
        self.rollouts = []
        self.rules = []

    def __setjson__(self, dct):
        self.target_id = dct.get('id')
        self.state = Converter.parse_bool(dct.get('state'))
        self.value = dct['value']
        self.is_rollout = Converter.parse_bool(dct.get('is_rollout'))
        self.rollouts = Converter.decode_json_list_of_class(dct.get('rollouts'), RolloutEntity)
        self.rules = Converter.decode_json_list_of_class(dct.get('rules'), RuleEntity)
