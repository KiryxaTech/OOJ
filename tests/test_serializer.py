import pytest
from ooj.serializer import Serializer


class Address:
    def __init__(self, street: str, city: str, zip_code: int):
        self.street = street
        self.city = city
        self.zip_code = zip_code

    def __eq__(self, other):
        if isinstance(other, Address):
            return (self.street == other.street and
                    self.city == other.city and
                    self.zip_code == other.zip_code)
        return False

class Person:
    def __init__(self, name: str, age: int, address: Address):
        self.name = name
        self.age = age
        self.address = address

    def __eq__(self, other):
        if isinstance(other, Person):
            return (self.name == other.name and
                    self.age == other.age and
                    self.address == other.address)
        return False


class Company:
    def __init__(self, company_name: str, employees: list[Person]):
        self.company_name = company_name
        self.employees = employees

    def __eq__(self, other):
        if isinstance(other, Company):
            return (self.company_name == other.company_name and
                    self.employees == other.employees)
        return False


class TestSerializer:
    @pytest.mark.parametrize("obj, expected_dict", [
        (
            Address(street="Main St", city="New York", zip_code=10001),
            {"street": "Main St", "city": "New York", "zip_code": 10001}
        ),
        (
            Person(name="John Doe", age=30, address=Address(street="Main St", city="New York", zip_code=10001)),
            {"name": "John Doe", "age": 30, "address": {"street": "Main St", "city": "New York", "zip_code": 10001}}
        ),
        (
            Company(
                company_name="TechCorp",
                employees=[
                    Person(name="John Doe", age=30, address=Address(street="Main St", city="New York", zip_code=10001)),
                    Person(name="Jane Smith", age=25, address=Address(street="Second St", city="Boston", zip_code=2215)),
                ]
            ),
            {
                "company_name": "TechCorp",
                "employees": [
                    {"name": "John Doe", "age": 30, "address": {"street": "Main St", "city": "New York", "zip_code": 10001}},
                    {"name": "Jane Smith", "age": 25, "address": {"street": "Second St", "city": "Boston", "zip_code": 2215}},
                ]
            }
        ),
    ])
    def test_serialize(self, obj, expected_dict):
        serialized_data = Serializer.serialize(obj)
        assert serialized_data == expected_dict

    @pytest.mark.parametrize("serialized_data, expected_obj", [
        (
            {"street": "Main St", "city": "New York", "zip_code": 10001},
            Address(street="Main St", city="New York", zip_code=10001)
        ),
        (
            {
                "name": "John Doe",
                "age": 30,
                "address": {"street": "Main St", "city": "New York", "zip_code": 10001}
            },
            Person(name="John Doe", age=30, address=Address(street="Main St", city="New York", zip_code=10001))
        ),
        (
            {
                "company_name": "TechCorp",
                "employees": [
                    {"name": "John Doe", "age": 30, "address": {"street": "Main St", "city": "New York", "zip_code": 10001}},
                    {"name": "Jane Smith", "age": 25, "address": {"street": "Second St", "city": "Boston", "zip_code": 2215}},
                ]
            },
            Company(
                company_name="TechCorp",
                employees=[
                    Person(name="John Doe", age=30, address=Address(street="Main St", city="New York", zip_code=10001)),
                    Person(name="Jane Smith", age=25, address=Address(street="Second St", city="Boston", zip_code=2215)),
                ]
            )
        ),
    ])
    def test_deserialize(self, serialized_data, expected_obj):
        deserialized_obj = Serializer.deserialize(serialized_data, type(expected_obj))
        assert deserialized_obj.__dict__ == expected_obj.__dict__
        if isinstance(expected_obj, Company):
            for emp_deserialized, emp_expected in zip(deserialized_obj.employees, expected_obj.employees):
                assert emp_deserialized.__dict__ == emp_expected.__dict__