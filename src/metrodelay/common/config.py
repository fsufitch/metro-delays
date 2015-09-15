import os, yaml

from metrodelay.common.util import working_directory

class Configuration(object):
    def __init__(self, main_conf_path):
        self.main_conf_path = main_conf_path
        self.files = {}
        self.register_file('root', self.main_conf_path)
        extras = self.get('extras', default={})
        self.load_extras(extras)

    def register_file(self, file_key, file_path):
        assert file_key not in self.files, "Config file '%s' already exists!" % file_key
        with open(file_path) as f:
            data = f.read()
        self.files[file_key] = ConfigurationFile(data)

    def load_extras(self, extras):
        full_path = os.path.realpath(self.main_conf_path)
        conf_dir = os.path.dirname(full_path)
        with working_directory(conf_dir):
            for filekey, path in extras.items():
                self.register_file(filekey, path)

    __no_default = []
    def get(self, *keys, filekey='root', default=__no_default):
        conf_file = self.files[filekey]
        if default is not Configuration.__no_default:
            return conf_file.get(*keys, default=default)
        else:
            return conf_file.get(*keys)

class ConfigurationFile(object):
    def __init__(self, data):
        self.data = yaml.load(data)
        
    __no_default = []

    def get(self, *keys, default=__no_default):
        current = self.data
        if not keys:
            raise TypeError("Must specify at least one key")
        for key in keys:
            try:
                current = current[key]
            except (KeyError, IndexError) as e:
                if default is not ConfigurationContainer.__no_default:
                    return default
                else:
                    raise e
        return current


            
