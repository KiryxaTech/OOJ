from ooj.json_serializer import JsonSerializer

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_values(self):
        print(f"{self.name}, {self.age} yars old.")

person = Person("Mike", 29)


def test_create_serializer():
    JsonSerializer({"ignore_errors": TypeError})

def test_serialize():
    serializer = JsonSerializer()
    serializer.serialize(person)