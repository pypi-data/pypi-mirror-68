import json
import logging
from importlib import reload

import pytest
import rtoml
from pydantic_loader import save_config
from pydantic_loader.config import CfgError, save_toml
from pydantic_loader.encode import encode_value
from tests import conf
from tests.conf import SomeConfig, DICT_DUMMY_CONFIG, DICT_NESTED_CONFIG

_LOGGER = logging.getLogger(__name__)


def validate_equivalence(value: conf.SomeConfig):
    expected = conf.SomeConfig()
    assert expected.a == value.a
    assert expected.b == value.b


dummy_js = {"a": 2, "b": "DEF"}
invalid_dummy_js = {"a": 10, "c": 5}


def toml_config_file(tmp_path):
    conf_file = tmp_path / "config_file.toml"
    with open(conf_file, "w") as fl:
        rtoml.dump(dummy_js, fl)
    return conf_file


def tml_config_file(tmp_path):
    conf_file = tmp_path / "config_file.tml"
    with open(conf_file, "w") as fl:
        rtoml.dump(dummy_js, fl)
    return conf_file


def json_config_file(tmp_path):
    conf_file = tmp_path / "config_file.json"
    with open(conf_file, "w") as fl:
        json.dump(dummy_js, fl)
    return conf_file

def real_toml_file(tmp_path):
    conf_file=tmp_path / "config_file.toml"
    toml_str = """
    a = 2
    # b = test
    b = "DEF"
    """
    with open(conf_file,"w") as fl:
        fl.write(toml_str)
    return conf_file

@pytest.fixture(params=[toml_config_file, json_config_file, tml_config_file,real_toml_file])
def config_file(request, tmp_path):
    return request.param(tmp_path)


@pytest.fixture
def invalid_config_file(tmp_path):
    conf_file = tmp_path / "config_file.json"
    with open(conf_file, "w") as fl:
        json.dump(invalid_dummy_js, fl)
    return conf_file


def test_unspecified_config():
    # todo: reloading does not work. once conf.CONFIG is defined it does not get reset.
    reload(conf)
    with pytest.raises(AttributeError):
        config = conf.CONFIG


def test_load_config_success(config_file):
    conf.CONFIG = conf.SomeConfig.load_config(config_file)
    assert isinstance(conf.CONFIG, conf.SomeConfig)


def test_load_config_not_found(tmp_path):
    """A non existing file is provided. Should return default config"""

    non_existing_config = tmp_path / "non_exist.json"

    _cfg = conf.SomeConfig.load_config(
        non_existing_config, on_error_return_default=True
    )

    validate_equivalence(_cfg)


def test_load_config_not_found_throw(tmp_path):
    """A non existing file is provided. Should raise exceptoin"""

    non_existing_config = tmp_path / "non_exist.json"

    with pytest.raises(CfgError):
        conf.SomeConfig.load_config(non_existing_config)


def test_load_config_file_success(config_file):
    _cfg = conf.SomeConfig.load_config(config_file)
    assert _cfg.a == dummy_js["a"]
    assert _cfg.b == dummy_js["b"]


def test_load_invalid_config(invalid_config_file):
    """Load an invalid config. Should return a default value"""
    _cfg = conf.SomeConfig.load_config(
        invalid_config_file, on_error_return_default=True
    )
    validate_equivalence(_cfg)


def test_load_invalid_config_raise(invalid_config_file):
    """Load an invalid config. Should raise a vaildation error."""
    with pytest.raises(CfgError):
        conf.SomeConfig.load_config(invalid_config_file)


def test_save_pydantic(tmp_path):
    """Saving a config and checking file existence"""

    new_file = tmp_path / "config.json"
    assert not new_file.exists()

    config = conf.SomeConfig()

    save_config(config, new_file)
    assert new_file.exists()


def test_save_toml(tmp_path):
    """Save a toml file and load it again."""
    toml_file = tmp_path / "config.toml"

    config = conf.NestedConfig()
    expected = config.dict()

    save_toml(config, toml_file)

    assert toml_file.exists()

    new_config = conf.NestedConfig.load_config(toml_file)
    assert isinstance(new_config.c, SomeConfig)

    result = new_config.dict()

    assert result["a"] == expected["a"]
    assert result["pth"] == expected["pth"]


def test_encode_value():
    config = conf.NestedConfig()
    dct = encode_value(config)

    assert dct == DICT_NESTED_CONFIG
    assert dct["dummy"] == DICT_DUMMY_CONFIG

def test_compare_to_dicts():
    """Compare dicts when done using custom function and with implemented .dict()"""
    config= conf.NestedConfig()
    result = json.dumps(encode_value(config))

    expected = config.json()

    assert result == expected
