
from codecs import BOM_UTF8
import logging

logger = logging.getLogger("floodgateio")


class Converter:

    @staticmethod
    def parse_bool(s):
        if isinstance(s, bool):
            return s
        return str(s).lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

    @staticmethod
    def parse_bool_or_value(val):
        slower = str(val).lower()
        if slower in ['true', 'y', 'yes']:
            return True
        if slower in ['false', 'n', 'no']:
            return False
        return val

    @staticmethod
    def lstrip_bom(str_, bom=BOM_UTF8):
        if str_.startswith(bom):
            return str_[len(bom):]
        return str_

    @staticmethod
    def decode_json_list_of_class(json_lst, class_type):
        return [Converter.decode_json_class(it, class_type) for it in json_lst or []]

    @staticmethod
    def decode_json_class(json_data, class_type):
        try:
            o = class_type.__new__(class_type)
            o.__setjson__(json_data)
        except Exception as e:
            logger.info("Failed to decode class {0}: [{1}] {2} -- from json: {3}".format(
                class_type, e.__class__.__name__, e, json_data
            ))
            raise
        return o
