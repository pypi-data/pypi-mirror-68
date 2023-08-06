# NoirPi JSON Handler

This is a simple JSON Filehandler. 

### Installation
```
pip install noirpi-jsonhandler
```

## FileIO Json Load
Load a JSON file
```
from jsonhandler.FileIO import FileIO

def load_json():
    FileIO("./test.json")
```
or creates the file with a given value.
If value is not given it uses an empty dict.
```
from jsonhandler.FileIO import FileIO

def load_json():
    FileIO("./test.json", {"test": True})
```
## FileIO Json Save
Save a JSON file
```
from jsonhandler.FileIO import FileIO

def save_json():
    file = FileIO("./test.json") 
    file.save()
```

## FileIO Json Replace
Replaces the content of a JSON file
```
from jsonhandler.FileIO import FileIO

def save_json():
    file = FileIO("./test.json") 
    file.replace({"test": True})
```

## FileIO Json File Check
Check if JSON file has valid Syntax
```
from jsonhandler.FileIO import FileIO

def check_json():
    file = FileIO("./test.json")
    file.is_valid_json()
```

## FileIO Json Dict Validation
Check if JSON dictionary is has a valid syntax
```
from jsonhandler.FileIO import validate

def validate_json():
    jsondict = {"test": "value"}
    validate(jsondict)
```

## FileIO get value 
Gets a value from JSON File
```
from jsonhandler.FileIO import FileIO

def get_value():
    file = FileIO("./test.json", {"test": {"key": True})
    file["test"]
    file["test", "key"]
```

## FileIO set value in json file
Sets or adds a value inside a JSON File
```
from jsonhandler.FileIO import FileIO

def get_value():
    file = FileIO("./test.json")
    file["test", "key"] = True
```
