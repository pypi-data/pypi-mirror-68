from hashlib import sha1


class EvaluatorHelper:

    @staticmethod
    def get_scale(key, user_id):
        # type: (str, str) -> int

        hash_str = key + user_id
        hash_sum = EvaluatorHelper.calc_hash_string(hash_str)[:7]
        return int(hash_sum, 16) % 100

    @staticmethod
    def calc_hash_string(unique_id):
        # type: (str) -> str
        h = sha1()
        h.update(unique_id.encode())
        return h.hexdigest()
