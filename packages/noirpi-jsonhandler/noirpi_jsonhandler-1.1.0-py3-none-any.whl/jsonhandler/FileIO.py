import json
import os
import traceback
from pathlib import Path
from random import randint
from typing import Dict

class Error(Exception):
    pass


# noinspection PySameParameterValue
class InvalidFileIOCall(Error):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
        try:
            self.io = args[1]
        except IndexError:
            self.io = None

    def __str__(self):
        if self.message:
            return '\nInvalidFileIOCall {0} "{1}" '.format(self.message, self.io)
        else:
            return 'InvalidFileIOCall has been raised'


class DataMustBeNone(Error):
    def __init__(self, *args):
        if args:
            self.io = args[0]
        else:
            self.io = None

    def __str__(self):
        if self.io:
            return 'Data must be None on option "{0}"'.format(self.io)
        else:
            return 'Data must be None on option -> "check" or "load"'


class DataCantBeNone(Error):
    def __init__(self, *args):
        if args:
            self.io = args[0]
        else:
            self.io = None

    def __str__(self):
        if self.io:
            return 'Data can\'t be None on option "{0}"'.format(self.io)
        else:
            return 'Data can\'t be None on option -> "save"'


class FileIO:
    def __init__(self, filepath, io, data=None):
        self.filepath = filepath
        self.io = io
        self.data = data

    @staticmethod
    def fileio(filepath, option, data=None):
        """
        :param filepath: Full Filepath including Filename
        :param option: action [save, load, check]
        :param data: json formatted data to save
        :return:
        """
        if option == "save":
            if data is not None:
                return FileIO._save_json(filepath, data)
            else:
                raise DataCantBeNone(option)
        elif option == "load":
            if data is None:
                return FileIO._read_json(filepath)
            else:
                raise DataMustBeNone(option)
        elif option == "check":
            if data is None:
                return FileIO._is_valid_json(filepath)
            else:
                raise DataMustBeNone(option)
        else:
            raise InvalidFileIOCall("FileIO was called with invalid parameter\n"
                                    "Allowed parameters are: 'save', 'load', and 'check'", option)

    @staticmethod
    def _is_valid_json(filepath):
        """Verifies if json file exists / is readable
        :param filepath Full Filepath including Filename"""
        try:
            FileIO._read_json(filepath)
            return True
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return False

    @staticmethod
    def validate(data: Dict):
        """Verifies json dict is readable
        :param data: json formatted data to validate"""
        tmp_file = "./{}.tmp".format(randint(1000, 9999))
        FileIO._dump_json(tmp_file, data)
        try:
            FileIO._read_json(tmp_file)
            os.remove(tmp_file)
            return True
        except json.decoder.JSONDecodeError as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return False

    @staticmethod
    def _read_json(filepath):
        """internally used function to read a json File
        :param filepath Full Filepath including Filename"""
        with open(filepath, encoding='utf-8', mode="r") as f:
            return json.loads(f.read())

    @staticmethod
    def _dump_json(filepath, data):
        """internally used function to read a json File
        :param filepath Full Filepath including Filename
        :param data: json formatted data to save"""
        with open(filepath, encoding='utf-8', mode="w") as f:
            json.dump(data, f, indent=4, sort_keys=True,
                      separators=(',', ' : '))
        return data

    # noinspection PySameParameterValue
    @staticmethod
    def _save_json(filepath, data):
        """Automically saves json file
        :param filepath Full Filepath including Filename
        :param data: json formatted data to save"""
        rnd = randint(1000, 9999)
        path, ext = os.path.splitext(filepath)
        tmp_file = "{}-{}.tmp".format(path, rnd)
        FileIO._dump_json(tmp_file, data)
        try:
            FileIO._read_json(tmp_file)
        except json.decoder.JSONDecodeError as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            print(f"Attempted to write file {filepath} but JSON integrity check on tmp file has failed.")
            print(f"The original file is unaltered.")
            return False
        os.replace(tmp_file, f"{filepath}")
        return True

    @staticmethod
    def check_file(path: str, filename: str, default_value):
        """check if file exists or create one
        :param path Path to file
        :param filename Filename
        :param default_value Default Value to input in a new created Json"""
        if not FileIO.fileio(f"{path}/{filename}", "check"):
            Path(path).mkdir(parents=True, exist_ok=True)
            print(f"Creating empty {filename}")
            FileIO.fileio(f"{path}/{filename}", "save", default_value)

    @staticmethod
    def get_value(filepath, *path):
        """get a value from a json File
        :param filepath Full filepath including Filename
        :param path Path inside the File (json standard use)"""
        _dict = FileIO.fileio(filepath, "load")
        for part in path:
            _dict = _dict[part]
        return _dict

    @staticmethod
    def set_value(filepath, add, *path):
        """get a value from a json File
        :param filepath Full filepath including Filename
        :param add Value to update or DICT to add into the json file
        :param path Path inside the File (json standard use)"""
        _dict = FileIO.fileio(filepath, "load")
        for part in path:
            try:
                if part == path[-1]:
                    _dict[part] = add
                elif not isinstance(_dict[part], dict):
                    _dict[part] = {}
                    _dict = _dict[part]
                else:
                    _dict = _dict[part]
            except KeyError:
                _dict[part] = {}
                _dict = _dict[part]
        FileIO.fileio(filepath, "save", _dict)
        return True
