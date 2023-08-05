import os
import json

from .utils import get_home_path


class SettingsHandler(object):
    
    config_dir = os.path.join(get_home_path(), ".easy_tools")
    config_file_name = "config.json"
    config_file_path = os.path.join(config_dir, config_file_name)
    os.makedirs(config_dir, exist_ok=True)
    if not os.path.exists(config_file_path):
        with open(config_file_path, "wb") as ff:
            ff.write(b"{}")
    with open(config_file_path, "r") as fr:
        content = fr.read()
        if not content:
            settings_json = {}
        else:
            settings_json = json.loads(content)

    @classmethod
    def read_property(cls, pro_path):
        temp = cls.settings_json
        for p in pro_path.split("."):
            temp = temp.get(p)
            if temp is None:
                # print("Maybe property path not exists! [{}]".format(pro_path))
                return temp
        return temp








