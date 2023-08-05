
from typing import Dict, Optional
from floodgateio.consts import Consts


class User:

    __user_id = None  # type: str
    email = None      # type: Optional[str]
    name = None       # type: Optional[str]
    custom_attributes = None # type: Dict[str,str]

    def __init__(self, user_id, email=None, name=None, custom_attributes=None):
        # type: (str, str, str, Dict[str,str]) -> None
        self.__user_id = user_id
        self.email = email
        self.name = name
        self.custom_attributes = custom_attributes or {}

    user_id = property(lambda self: self.__user_id)

    def get_attribute_value(self, key):
        # type: (str) -> Optional[str]
        key = key.lower()

        if key == Consts.USER_ATTRIBUTE_ID.lower():
            return self.user_id

        if key == Consts.USER_ATTRIBUTE_EMAIL.lower():
            return self.email

        if key == Consts.USER_ATTRIBUTE_NAME.lower():
            return self.name

        values = [v for k, v in self.custom_attributes.items() if k.lower() == key]
        if values:
            return values[0]

        return None
