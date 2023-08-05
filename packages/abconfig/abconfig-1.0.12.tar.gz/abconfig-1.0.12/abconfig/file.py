import json

try:
    import yaml
except ImportError:
    pass

try:
    import toml
except ImportError:
    pass

from os.path import splitext
from configparser import ConfigParser

from abconfig.common import Dict


class Reader(Dict):
    def __init__(self, obj: Dict):
        self._fail = False
        self._path = obj.get('__file__')
        if self._path:
            prefix = obj.get('__prefix__', None)
            if prefix:
                super().__init__(obj + self._read[prefix])
            else:
                super().__init__(obj + self._read)
        else:
            super().__init__(obj)

    @property
    def _read(self) -> dict:
        try:
            with open(self._path, 'r') as fd:
                result = self._driver(fd)
                if not self.is_dict(result):
                    raise IOError
                return result
        except Exception:
            self._fail = True
            return self.__mempty__

    def _driver(self, fd) -> dict:
        raise NotImplementedError


class Yaml(Reader):
    __extensions__ = ('yml', 'yaml')

    def _driver(self, fd) -> dict:
        return yaml.load(fd, Loader=yaml.FullLoader)


class Json(Reader):
    __extensions__ = ('json',)

    def _driver(self, fd) -> dict:
        return json.load(fd)


class Toml(Reader):
    __extensions__ = ('toml',)

    def _driver(self, fd) -> dict:
        return toml.load(fd)


class Ini(Reader):
    __extensions__ = ('ini',)

    @property
    def _read(self) -> dict:
        driver = ConfigParser()
        driver.read(self._path)
        return driver._sections


class Format(type):
    def __call__(cls, obj: Dict) -> Dict:
        enabled = obj.get('__file__', None)
        if enabled:
            return cls._format(obj, enabled, cls.__formats__)
        else:
            return obj

    @staticmethod
    def _format(obj: Dict, path: str, formats: tuple) -> tuple:
        _, extension = splitext(path)
        for format_ in formats:
            for e in format_.__extensions__:
                if e == extension[1:]:
                    return obj.bind(format_)

        for format_ in formats:
            new = obj.bind(format_)
            if new._fail is False:
                return new

        if obj.get('__file_required__') is True:
            raise FileNotFoundError

        return obj


class File(metaclass=Format):
    __formats__ = (Json, Yaml, Toml, Ini)
