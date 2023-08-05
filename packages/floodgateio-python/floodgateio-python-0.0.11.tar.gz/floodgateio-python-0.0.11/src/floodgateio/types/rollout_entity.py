

class RolloutEntity:

    value = None  # type: str
    percentage = 0  # type: int

    def __setjson__(self, dct):
        self.value = dct['value']
        self.percentage = int(dct['percentage'])
