from ooj.json_serilizer import JsonSerializer

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

    new_person: Person = serializer.deserialize(person, Person)

    assert person.name == new_person.name