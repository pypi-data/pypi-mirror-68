from enum import Enum, unique
from six import string_types


@unique
class Collection(Enum):
    RACE = 1
    ALLEN_AI_DROP = 2
    CSQA = 3  # https://www.tau-nlp.org/commonsenseqa
    ALLEN_AI_OBQA = 4  # https://github.com/allenai/OpenBookQA

    @staticmethod
    def from_str(label):
        assert(isinstance(label, string_types))
        value = None
        try:
            value = Collection[label]
        except KeyError:
            pass

        if value is None:
            raise NotImplementedError(
                    "Dataset `{}` is not part of the collection.".format(label)
            )
        return value
