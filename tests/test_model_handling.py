from collections import deque
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID, uuid4

import pytest
from faker import Faker
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    ByteSize,
    DirectoryPath,
    EmailStr,
    FilePath,
    HttpUrl,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    Json,
    NameEmail,
    NegativeFloat,
    NegativeInt,
    NonNegativeInt,
    NonPositiveFloat,
    PaymentCardNumber,
    PositiveFloat,
    PositiveInt,
    PostgresDsn,
    PyObject,
    RedisDsn,
    SecretBytes,
    SecretStr,
    StrictBool,
    StrictBytes,
    StrictFloat,
    StrictInt,
    StrictStr,
    conbytes,
    condecimal,
    confloat,
    conint,
    conlist,
    conset,
    constr,
)
from pydantic.color import Color

from pydantic_factories.exceptions import ConfigurationError
from pydantic_factories.factory import ModelFactory


class Pet(BaseModel):
    name: str
    species: str
    color: str
    sound: str
    age: float


class Person(BaseModel):
    id: UUID
    name: str
    hobbies: Optional[List[str]] = None
    age: Union[float, int]
    pets: List[Pet]
    birthday: Union[datetime, date]


class PersonFactory(ModelFactory):
    __model__ = Person

    id = uuid4()
    model = Person
    name = "moishe"
    hobbies = ["fishing"]
    age = 33
    pets = []
    birthday = datetime(2021 - 33, 1, 1)


class PetFactory(ModelFactory):
    __model__ = Pet


def test_init_validation():
    with pytest.raises(ConfigurationError):

        class MyFactory(ModelFactory):
            pass

        MyFactory.build()


def test_init_faker_override():
    my_faker = Faker()
    setattr(my_faker, "__test__attr__", None)

    class MyFactory(ModelFactory):
        __model__ = Pet
        __faker__ = my_faker

    assert hasattr(MyFactory.get_faker(), "__test__attr__")


def test_merges_defaults_with_kwargs():
    first_obj = PersonFactory.build()
    assert first_obj.id == PersonFactory.id
    assert first_obj.name == PersonFactory.name
    assert first_obj.hobbies == PersonFactory.hobbies
    assert first_obj.age == PersonFactory.age
    assert first_obj.pets == PersonFactory.pets
    assert first_obj.birthday == PersonFactory.birthday
    pet = Pet(
        name="bluey the blowfish",
        species="blowfish",
        color="bluish-green",
        sound="",
        age=1,
    )
    new_id = uuid4()
    new_hobbies = ["dancing"]
    new_age = 35
    new_pets = [pet]
    second_obj = PersonFactory.build(id=new_id, hobbies=new_hobbies, age=new_age, pets=new_pets)
    assert second_obj.id == new_id
    assert second_obj.hobbies == new_hobbies
    assert second_obj.age == new_age
    assert second_obj.pets == [pet]
    assert second_obj.name == PersonFactory.name
    assert second_obj.birthday == PersonFactory.birthday


def test_respects_none_overrides():
    result = PersonFactory.build(hobbies=None)
    assert result.hobbies is None


def test_uses_faker_to_set_values_when_none_available_on_class():
    result = PetFactory.build()
    assert isinstance(result.name, str)
    assert isinstance(result.species, str)
    assert isinstance(result.color, str)
    assert isinstance(result.sound, str)
    assert isinstance(result.age, float)


def test_builds_batch():
    results = PetFactory.batch(10)
    assert isinstance(results, list)
    assert len(results) == 10
    for result in results:
        assert isinstance(result.name, str)
        assert isinstance(result.species, str)
        assert isinstance(result.color, str)
        assert isinstance(result.sound, str)
        assert isinstance(result.age, float)


def test_type_property_parsing():
    class MyModel(BaseModel):
        float_field: float
        int_field: int
        bool_field: bool
        str_field: str
        bytes_field: bytes
        # built-in objects
        dict_field: dict
        tuple_field: tuple
        list_field: list
        set_field: set
        frozenset_field: frozenset
        deque_field: deque
        # standard library objects
        Path_field: Path
        Decimal_field: Decimal
        UUID_field: UUID
        # datetime
        datetime_field: datetime
        date_field: date
        time_field: time
        timedelta_field: timedelta
        # ip addresses
        IPv4Address_field: IPv4Address
        IPv4Interface_field: IPv4Interface
        IPv4Network_field: IPv4Network
        IPv6Address_field: IPv6Address
        IPv6Interface_field: IPv6Interface
        IPv6Network_field: IPv6Network
        # pydantic specific
        ByteSize_pydantic_type: ByteSize
        PositiveInt_pydantic_type: PositiveInt
        FilePath_pydantic_type: FilePath
        NegativeFloat_pydantic_type: NegativeFloat
        NegativeInt_pydantic_type: NegativeInt
        PositiveFloat_pydantic_type: PositiveFloat
        NonPositiveFloat_pydantic_type: NonPositiveFloat
        NonNegativeInt_pydantic_type: NonNegativeInt
        StrictInt_pydantic_type: StrictInt
        StrictBool_pydantic_type: StrictBool
        StrictBytes_pydantic_type: StrictBytes
        StrictFloat_pydantic_type: StrictFloat
        StrictStr_pydantic_type: StrictStr
        DirectoryPath_pydantic_type: DirectoryPath
        EmailStr_pydantic_type: EmailStr
        NameEmail_pydantic_type: NameEmail
        PyObject_pydantic_type: PyObject
        Color_pydantic_type: Color
        Json_pydantic_type: Json
        PaymentCardNumber_pydantic_type: PaymentCardNumber
        AnyUrl_pydantic_type: AnyUrl
        AnyHttpUrl_pydantic_type: AnyHttpUrl
        HttpUrl_pydantic_type: HttpUrl
        PostgresDsn_pydantic_type: PostgresDsn
        RedisDsn_pydantic_type: RedisDsn
        UUID1_pydantic_type: UUID1
        UUID3_pydantic_type: UUID3
        UUID4_pydantic_type: UUID4
        UUID5_pydantic_type: UUID5
        SecretBytes_pydantic_type: SecretBytes
        SecretStr_pydantic_type: SecretStr
        IPvAnyAddress_pydantic_type: IPvAnyAddress
        IPvAnyInterface_pydantic_type: IPvAnyInterface
        IPvAnyNetwork_pydantic_type: IPvAnyNetwork

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()

    for key in MyFactory.get_provider_map().keys():
        if hasattr(result, f"{key.__name__}_field"):
            assert isinstance(getattr(result, f"{key.__name__}_field"), key)
        elif hasattr(result, f"{key.__name__}_pydantic_type"):
            assert getattr(result, f"{key.__name__}_pydantic_type") is not None


def test_constrained_property_parsing():
    class MyModel(BaseModel):
        conbytes_field: conbytes()
        condecimal_field: condecimal()
        confloat_field: confloat()
        conint_field: conint()
        conlist_field: conlist(str)
        conset_field: conset(str)
        constr_field: constr()

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()

    assert isinstance(result.conbytes_field, bytes)
    assert isinstance(result.constr_field, str)
    assert isinstance(result.conint_field, int)
    assert isinstance(result.confloat_field, float)
    assert isinstance(result.condecimal_field, Decimal)
    assert isinstance(result.conlist_field, list)
    assert isinstance(result.conset_field, set)