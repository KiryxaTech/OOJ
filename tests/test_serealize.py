import json

from ooj.json_serializer import JsonSerializer


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_values(self):
        print(f"{self.name}, {self.age} yars old.")

person = Person("Mike", 29)


def test_create_serializer():
    serializer = JsonSerializer({"ignore_errors": TypeError})

    assert serializer.get_serialization_options() == {"ignore_errors": TypeError}


def test_serialize():
    serializer = JsonSerializer()
    serialize_person = serializer.serialize(person)

    assert serialize_person == '{"name": "Mike", "age": 29}'


def test_deserialize():
    serializer = JsonSerializer()
    serializer.serialize(person)

    deserialize_person: Person = serializer.deserialize(person, Person)

    assert person.name == deserialize_person.name


def test_serialize_to_file():
    serialize_file_path = 'tests\\files\\serialize_obj.json'

    serializer = JsonSerializer()
    serializer.serialize_to_file(person, serialize_file_path)

    with open(serialize_file_path, 'r', encoding='utf-8') as f:
        serialize_data = json.load(f)

    assert serialize_data == {"name": "Mike", "age": 29}


def test_deserialize_from_file():
    serialize_file_path = 'tests\\files\\serialize_obj.json'

    serializer = JsonSerializer()
    deserialize_person: Person = serializer.deserialize_from_file(serialize_file_path, Person)

    assert person.age == deserialize_person.age