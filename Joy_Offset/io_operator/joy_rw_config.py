import contextlib
import io
import json
import os

from jsonschema import validate


try:
    cwd = os.path.join(os.path.expanduser(os.getenv('USERPROFILE')), 'AppData', 'Local', 'Joy_Offset', 'Settings')        
    os.makedirs(cwd, exist_ok = True)
except:
    cwd = 'data'

finally:
    default_data = {
        "usages": {
            "use_l_analog": True, 
            "use_r_analog": True,
            "use_l_trigger": True,
            "use_r_trigger": True,
            "replicate_btns": True,
            "joy_id": 1        
            },

        "offsets": {
            "l_analog_offset_x": 0.0,
            "l_analog_offset_y": 0.0,
            "r_analog_offset_x": 0.0,
            "r_analog_offset_y": 0.0,
            "l_trigger_offset": -1.0,
            "r_trigger_offset": -1.0 
            }
        }
    
    expected_keys_types = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "usages": {
            "type": "object",
            "properties": {
                "use_l_analog": {
                "type": "boolean"
                },
                "use_r_analog": {
                "type": "boolean"
                },
                "use_l_trigger": {
                "type": "boolean"
                },
                "use_r_trigger": {
                "type": "boolean"
                },
                "replicate_btns": {
                "type": "boolean"
                },
                "joy_id": {
                "type": "integer"
                }
            },
            "required": [
                "use_l_analog",
                "use_r_analog",
                "use_l_trigger",
                "use_r_trigger",
                "replicate_btns",
                "joy_id"
            ]
            },
            "offsets": {
            "type": "object",
            "properties": {
                "l_analog_offset_x": {
                "type": "number"
                },
                "l_analog_offset_y": {
                "type": "number"
                },
                "r_analog_offset_x": {
                "type": "number"
                },
                "r_analog_offset_y": {
                "type": "number"
                },
                "l_trigger_offset": {
                "type": "number"
                },
                "r_trigger_offset": {
                "type": "number"
                }
            },
            "required": [
                "l_analog_offset_x",
                "l_analog_offset_y",
                "r_analog_offset_x",
                "r_analog_offset_y",
                "l_trigger_offset",
                "r_trigger_offset"
            ]
            }
        },
        "required": ["usages", "offsets"]
    }

    full_path = os.path.join(cwd, 'config.json')
   
    
def validate_keys(data, expected):
    try:    
        for key, value in expected.items():
            if key not in data:
                return False
            
            elif isinstance(value, dict):
                validate_keys(data[key], value)
                
            elif not isinstance(data[key], value):
                return False            
        return True
    except: 
        return False
         
            
def read_config():        
    if not os.path.exists(full_path):
        write_config(default_data)
            
        return default_data
    else:
        try:
            with contextlib.ExitStack() as stack:
                file = stack.enter_context(io.open(full_path, mode='r', encoding='utf-8'))
                data = json.load(file)     
            try:
                validate(instance = data, schema = expected_keys_types)
                
                return data         
            except:
                raise Exception      
        except:
            write_config(default_data)      
            return default_data
    
        
def write_config(context):
    try:
        with contextlib.ExitStack() as stack:
            file = stack.enter_context(open(full_path, mode='w', encoding='utf-8'))
            json.dump(context, file, indent=4)
            
        return True
    except:
        return False
