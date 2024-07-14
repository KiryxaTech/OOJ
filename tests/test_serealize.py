import json

from ooj.json_serializer import JsonSerializer
from ooj.exceptions import NotSerializableException

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_values(self):
        print(f"{self.name}, {self.age} years old.")

person = Person("Mike", 29)


def test_create_serializer():
    serializer = JsonSerializer({"ignore_errors": NotSerializableException, "indent": 4})

    assert serializer.get_serialization_options()["ignore_errors"] == NotSerializableException
    assert serializer.get_serialization_options()["indent"] == 4


def test_serialize():
    serializer = JsonSerializer()
    serialize_person = serializer.serialize(person)

    assert serialize_person == '{"name": "Mike", "age": 29}'


def test_deserialize():
    serializer = JsonSerializer()
    serializer.serialize(person)

    deserialize_person: Person = serializer.deserialize(person, Person)

    assert person.name == deserialize_person.name
    assert person.age == deserialize_person.age
    assert person.get_values() == deserialize_person.get_values()


def test_serialize_to_file():
    serialize_file_path = 'tests\\files\\serialize_obj.json'

    serializer = JsonSerializer()
    serializer.serialize_to_file(person, serialize_file_path)

    with open(serialize_file_path, 'r', encoding='utf-8') as f:
        serialize_data = json.load(f)

    assert serialize_data["name"] == "Mike"
    assert serialize_data["age"] == 29


def test_deserialize_from_file():
    serialize_file_path = 'tests\\files\\serialize_obj.json'

    serializer = JsonSerializer()
    deserialize_person: Person = serializer.deserialize_from_file(serialize_file_path, Person)

    assert person.name == deserialize_person.name
    assert person.age == deserialize_person.age
    assert person.get_values() == deserialize_person.get_values()