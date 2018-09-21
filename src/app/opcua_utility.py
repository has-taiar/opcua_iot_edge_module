from datetime import datetime as dt
import uuid as uid

from opcua import ua


def map_to_opcua_type_and_value(type_identifier, desired_value): 
    if type_identifier < 0 or type_identifier > 14: 
        raise ValueError('Error: The type_identifier needs to be between 0-25. Current implementation only supports 0-14. For more info see: https://github.com/FreeOpcUa/python-opcua/blob/master/opcua/ua/uatypes.py#L619')
    map_table = {}
    map_table[0] = {'type': ua.VariantType.Null, 'converter': lambda a: None}
    map_table[1] = {'type': ua.VariantType.Boolean, 'converter': lambda a: bool(a) }
    map_table[2] = {'type': ua.VariantType.SByte, 'converter': lambda a: int(a) }
    map_table[3] = {'type': ua.VariantType.Byte, 'converter': lambda a: int(a) }
    map_table[4] = {'type': ua.VariantType.Int16, 'converter': lambda a: int(a) }
    map_table[5] = {'type': ua.VariantType.UInt16, 'converter': lambda a: int(a) }
    map_table[6] = {'type': ua.VariantType.Int32, 'converter': lambda a: int(a) }
    map_table[7] = {'type': ua.VariantType.UInt32, 'converter': lambda a: int(a) }
    map_table[8] = {'type': ua.VariantType.Int64, 'converter': lambda a: int(a) }
    map_table[9] = {'type': ua.VariantType.UInt64, 'converter': lambda a: int(a) }
    map_table[10] = {'type': ua.VariantType.Float, 'converter': lambda a: float(a) }
    map_table[11] = {'type': ua.VariantType.Double, 'converter': lambda a: float(a) }
    map_table[12] = {'type': ua.VariantType.String, 'converter': lambda a: a }
    map_table[13] = {'type': ua.VariantType.DateTime, 'converter': lambda a: dt.strptime(a, "%Y-%m-%d %H:%M:%S") }
    map_table[14] = {'type': ua.VariantType.Guid, 'converter': lambda a: uid.UUID(a) }
    
    opc_type = map_table[type_identifier]['type']
    parsed_value = map_table[type_identifier]['converter'](desired_value) 
    
    return parsed_value, opc_type
