import os
import pytest
from pathlib import Path
from ooj.json_file import JsonFile


# Base path from test JSON files
BASE_PATH = Path('tests/files/test_json_files')


class TestJsonFile:
    @pytest.mark.parametrize(
        "file_path",
        [
            BASE_PATH / "created_file.json",
            BASE_PATH / "not_created_file.json"
        ]
    )
    def test_create_if_not_exists(self, file_path):
        JsonFile(file_path)

        assert file_path.exists()

    @pytest.mark.parametrize(
        "file_path",
        [
            BASE_PATH / "delete.json"
        ]
    )
    def test_delete(self, file_path):
        file = JsonFile(file_path)
        file.delete()
        assert not file_path.exists()

    @pytest.mark.parametrize(
        "keys_path, value",
        [
            ("key_1", "value_1"),
            (["key_2", "nested_key_2"], "value_2"),
            ("new_key", "new_value")
        ]
    )
    def test_set_value(self, keys_path, value):
        file = JsonFile(BASE_PATH / "set_value.json")
        file.set_value(keys_path, value)
        assert file.get_value(keys_path) == value

    @pytest.mark.parametrize(
        "keys_path, expected_value",
        [
            ("key", "value"),
            (["keys", "nested_key"], "nested_value")
        ]
    )
    def test_get_value(self, keys_path, expected_value):
        file = JsonFile(BASE_PATH / "get_value.json")
        assert file.get_value(keys_path) == expected_value

    @pytest.mark.parametrize(
        "keys_path",
        [
            "key",
            ["keys", "nested_key"]
        ]
    )
    def test_remove_key(self, keys_path):
        file = JsonFile(BASE_PATH / "remove_key.json")
        file.set_value(keys_path, "dummy_value")
        file.remove_key(keys_path)
        with pytest.raises(KeyError):
            file.get_value(keys_path)