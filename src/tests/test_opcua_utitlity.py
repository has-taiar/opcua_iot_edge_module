import pytest

from opcua import ua
import uuid as uid
from datetime import datetime

from app import opcua_utility as utility


def test_when_passed_in_identifier_as_0_should_parse_to_null():
    value, opc_type = utility.map_to_opcua_type_and_value(0, '')
    assert value is None
    assert opc_type == ua.VariantType.Null


def test_when_passed_in_identifier_as_1_should_parse_to_boolean():
    value, opc_type = utility.map_to_opcua_type_and_value(1, 'true')
    assert type(value) is bool
    assert value is True
    assert opc_type == ua.VariantType.Boolean


def test_when_passed_in_identifier_as_2_should_parse_to_sbyte():
    value, opc_type = utility.map_to_opcua_type_and_value(2, '1')
    assert type(value) is int
    assert value is 1
    assert opc_type == ua.VariantType.SByte


def test_when_passed_in_identifier_as_3_should_parse_to_byte():
    value, opc_type = utility.map_to_opcua_type_and_value(3, '1')
    assert type(value) is int
    assert value is 1
    assert opc_type == ua.VariantType.Byte


def test_when_passed_in_identifier_as_4_should_parse_to_int16():
    value, opc_type = utility.map_to_opcua_type_and_value(4, '44')
    assert type(value) is int
    assert opc_type == ua.VariantType.Int16


def test_when_passed_in_identifier_as_5_should_parse_to_uint16():
    value, opc_type = utility.map_to_opcua_type_and_value(5, '55')
    assert type(value) is int
    assert opc_type == ua.VariantType.UInt16


def test_when_passed_in_identifier_as_6_should_parse_to_int32():
    value, opc_type = utility.map_to_opcua_type_and_value(6, '66')
    assert type(value) is int
    assert opc_type == ua.VariantType.Int32


def test_when_passed_in_identifier_as_7_should_parse_to_uint32():
    value, opc_type = utility.map_to_opcua_type_and_value(7, '77')
    assert type(value) is int
    assert opc_type == ua.VariantType.UInt32


def test_when_passed_in_identifier_as_8_should_parse_to_int64():
    value, opc_type = utility.map_to_opcua_type_and_value(8, '88')
    assert type(value) is int
    assert opc_type == ua.VariantType.Int64


def test_when_passed_in_identifier_as_9_should_parse_to_uint64():
    value, opc_type = utility.map_to_opcua_type_and_value(9, '99')
    assert type(value) is int
    assert opc_type == ua.VariantType.UInt64


def test_when_passed_in_identifier_as_10_should_parse_to_float():
    value, opc_type = utility.map_to_opcua_type_and_value(10, '100.0')
    assert type(value) is float
    assert opc_type == ua.VariantType.Float


def test_when_passed_in_identifier_as_11_should_parse_to_double():
    value, opc_type = utility.map_to_opcua_type_and_value(11, '100.11')
    assert type(value) is float
    assert opc_type == ua.VariantType.Double


def test_when_passed_in_identifier_as_12_should_parse_to_string():
    value, opc_type = utility.map_to_opcua_type_and_value(12, 'I am a string')
    assert type(value) is str
    assert opc_type == ua.VariantType.String


def test_when_passed_in_identifier_as_13_should_parse_to_datetime():
    value, opc_type = utility.map_to_opcua_type_and_value(13, '2018-08-15 10:10:00')
    print(str(value))
    assert type(value) is datetime
    assert opc_type == ua.VariantType.DateTime


def test_when_passed_in_identifier_as_14_should_parse_to_guid():
    value, opc_type = utility.map_to_opcua_type_and_value(14, '3ca5c721-cb26-4be5-92a5-ac6f413113be')
    assert type(value) is uid.UUID
    assert opc_type == ua.VariantType.Guid

# TODO: we should add more tests for routes