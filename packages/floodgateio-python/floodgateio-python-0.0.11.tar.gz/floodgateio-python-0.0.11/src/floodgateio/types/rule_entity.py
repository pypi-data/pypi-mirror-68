
from typing import List
from floodgateio.utils.converter import Converter


class RuleEntity:

    rule_id = None  # type: str
    attribute = None  # type: str
    comparator = 0  # type: int
    values = None  # type: List[str]

    def __init__(self):
        self.values = []

    def __setjson__(self, dct):
        self.rule_id = dct.get('id')
        self.attribute = dct.get('attribute')
        self.comparator = dct.get('comparator') or 0
        self.values = dct.get('values') or []
