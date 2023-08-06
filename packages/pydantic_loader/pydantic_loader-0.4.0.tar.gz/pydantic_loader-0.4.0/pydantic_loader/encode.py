import logging
from typing import Any

from pydantic.json import pydantic_encoder

_LOGGER = logging.getLogger(__name__)


def loop_over_list(lst) -> list:
    new_list = []
    for itm in lst:
        new_list.append(encode_value(itm))
    return new_list


def loop_over_dict(obj) -> dict:
    new_dict = {}
    for key, value in obj.items():
        new_dict[key] = encode_value(value)
    return new_dict


def encode_value(obj: Any):
    try:
        result = pydantic_encoder(obj)
    except TypeError:
        if any(
            (
                isinstance(obj, str),
                isinstance(obj, bool),
                isinstance(obj, int),
                isinstance(obj, float),
                isinstance(obj, bytes),
            )
        ):
            return obj
        elif isinstance(obj, dict):
            return loop_over_dict(obj)
        elif isinstance(obj, list):
            return loop_over_list(obj)
        else:
            raise
    else:
        if isinstance(result, dict):
            return loop_over_dict(result)
        return encode_value(result)
    raise TypeError(f"Unknown type has appeared {obj.__class__.__name__}")