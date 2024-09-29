import pytest
import json
from ooj.exceptions import NotSerializableException
from ooj.serializer import JsonSerializer


class SampleClass:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ComplexClass:
    def __init__(self, id, data):
        self.id = id
        self.data = data


class TestJsonSerializer:
    @pytest.fixture
    def serializer(self):
        return JsonSerializer()

    @pytest.mark.parametrize("obj, expected_json", [
        (SampleClass(name="test", value=123), '{"name": "test", "value": 123}'),
        (SampleClass(name="example", value=456), '{"name": "example", "value": 456}'),
        (ComplexClass(id=1, data={"key": "value"}), '{"id": 1, "data": {"key": "value"}}'),
    ])
    def test_serialize(self, serializer, obj, expected_json):
        json_str = serializer.serialize(obj)
        assert json.loads(json_str) == json.loads(expected_json)

    @pytest.mark.parametrize("json_str, cls, expected_obj", [
        ('{"name": "test", "value": 123}', SampleClass, SampleClass(name="test", value=123)),
        ('{"name": "example", "value": 456}', SampleClass, SampleClass(name="example", value=456)),
        ('{"id": 1, "data": {"key": "value"}}', ComplexClass, ComplexClass(id=1, data={"key": "value"})),
    ])
    def test_deserialize(self, serializer, json_str, cls, expected_obj):
        obj = serializer.deserialize(json_str, cls)
        assert obj.__dict__ == expected_obj.__dict__

    @pytest.mark.parametrize("obj, file_content", [
        (SampleClass(name="test", value=123), '{"name": "test", "value": 123}'),
        (SampleClass(name="example", value=456), '{"name": "example", "value": 456}'),
        (ComplexClass(id=1, data={"key": "value"}), '{"id": 1, "data": {"key": "value"}}'),
    ])
    def test_serialize_to_file(self, serializer, obj, file_content, tmp_path):
        file_path = tmp_path / "test.json"
        serializer.serialize_to_file(obj, str(file_path))
        with open(file_path, "r", encoding="utf-8") as f:
            assert json.load(f) == json.loads(file_content)

    @pytest.mark.parametrize("file_content, cls, expected_obj", [
        ('{"name": "test", "value": 123}', SampleClass, SampleClass(name="test", value=123)),
        ('{"name": "example", "value": 456}', SampleClass, SampleClass(name="example", value=456)),
        ('{"id": 1, "data": {"key": "value"}}', ComplexClass, ComplexClass(id=1, data={"key": "value"})),
    ])
    def test_deserialize_from_file(self, serializer, file_content, cls, expected_obj, tmp_path):
        file_path = tmp_path / "test.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        obj = serializer.deserialize_from_file(str(file_path), cls)
        assert obj.__dict__ == expected_obj.__dict__

    def test_handle_not_serializable(self, serializer):
        with pytest.raises(NotSerializableException):
            serializer.serialize(object())