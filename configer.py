# -*- coding: utf8 -*- 

__author__ = "A. Daouzli"
__copyright__ = "2016, A. Daouzli"
__version__ = "0.0.1"
__maintainer__ = "A. Daouzli"

import types


class ConfigGetter(object):
    def __init__(self, filename, no_exception=True):
        """
        :param filename: the configuration file name
        :param no_exception: if True won't raise an exception if try to access
        a non existent parameter but will return None. (default True)
        """
        self.get_config_from_file(filename)
        self._no_exception = no_exception

    def __getattr__(self, name):
        if self._no_exception:
            return None
        else:
            return object.__getattribute__(self, name)

    def _build_value(self, prevalue):
        tmp_value = ""
        while prevalue:
            if not prevalue.startswith('"'):
                tmp = prevalue.split(" + ", 1)
                if len(tmp) > 1:
                    elem, prevalue = map(lambda x: x.strip(), tmp)
                else:
                    elem = tmp[0]
                    prevalue = ""
                if elem in self.__dict__:
                    tmp_value += self.__dict__[elem]
                else:
                    raise Exception("Reference '{0}' not defined in configuration file".format(elem))
            else:
                i = prevalue[1:].find('"') + 1
                tmp_value += prevalue[1:i].strip()
                prevalue = prevalue[i + 1:].strip()
                if prevalue.startswith('+'):
                    prevalue = prevalue[1:].strip()
        return tmp_value

    def get_all(self):
        res = {}
        for k, v in self.__dict__.items():
            if not type(v) is types.MethodType and not v.startswith("_"):
                res[k] = v
        return res

    def get_config_from_file(self, filename):
        """Get configuration from file
        :param filename: the configuration file name
        """
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#") or line.strip() == "":
                    continue
                if line.startswith("%include"):
                    prevalue = line.replace("%include", "").strip()
                    if prevalue.startswith('"') and prevalue.endswith('"'):
                        conf = prevalue[1:-1]
                    else:
                        conf = self._build_value(prevalue)
                    self.get_config_from_file(conf)
                else:
                    field, prevalue = map(lambda x: x.strip(), line.split("=", 1))
                    if prevalue.startswith('"') and prevalue.endswith('"'):
                        value = prevalue[1:-1]
                    else:
                        value = self._build_value(prevalue)
                    self.__dict__[field] = value


