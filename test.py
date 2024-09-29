from typing import List, Tuple

from ooj.serializer import Serializer, Field


class Pet:
    def __init__(self, name):
        self.name = name


class Person:
    def __init__(self, name, age, pet: Pet = None, data = None):
        self.name = name
        self.age = age
        self.pet = pet
        self.data = data

class Ticket:
    def __init__(self, persons: List[Person], seat: str):
        self.persons = persons
        self.seat = seat


def main():
    ticket_seria = {
        "persons": [
            {
                "name": "Kitty",
                "age": 13,
                "pet": Pet("Dog"),
                "data": {
                    "data": "value"
                }
            },
            {
                "name": "Jo Baiden",
                "age": 78
            }
        ],
        "seat": "a18"
    }
    ticket_types = {
        "persons": Field(Tuple[Person], {"pet": Pet})
    }

    ticket: Ticket = Serializer.deserialize(ticket_seria, Ticket)
    person: Person = ticket.persons[0]
    name = person.name
    age = person.age
    pet_name = person.pet.name
    data = person.data

    print(f"Имя: {name}, возраст: {age} лет, питомец: {pet_name}, инфо: {data}")

if __name__ == "__main__":
    main()