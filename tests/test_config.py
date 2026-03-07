import pytest
import pathlib
import yaml
from media_organizer.config import Config

def test_config_init_default():
    config = Config()
    assert config.config_path == pathlib.Path("config.yaml")
    assert config.data == {}

def test_config_init_custom():
    config = Config("custom_config.yaml")
    assert config.config_path == pathlib.Path("custom_config.yaml")
    assert config.data == {}

def test_config_load_success(tmp_path):
    config_file = tmp_path / "config.yaml"
    data = {"key": "value", "nested": {"a": 1}}
    with open(config_file, "w") as f:
        yaml.dump(data, f)

    config = Config(str(config_file))
    loaded_data = config.load()

    assert loaded_data == data
    assert config.data == data

def test_config_load_file_not_found(tmp_path):
    config_file = tmp_path / "non_existent.yaml"
    config = Config(str(config_file))
    with pytest.raises(FileNotFoundError):
        config.load()

def test_config_load_invalid_yaml(tmp_path):
    config_file = tmp_path / "invalid.yaml"
    with open(config_file, "w") as f:
        f.write("invalid: yaml: :")

    config = Config(str(config_file))
    with pytest.raises(yaml.YAMLError):
        config.load()
