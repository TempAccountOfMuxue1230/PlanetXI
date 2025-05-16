"""
File: config.py
File Version: 1.0
"""
import helper.binary as jb_helper
import json
import os


class Config:
    """
    Class Name: Config
    Class Description: Read and compile correct configuration files
    """
    DEFAULT = {
        "game_basic": {
            "window": {
                "width": 0,
                "height": 0
            },
            "sound": {
                "volume": 100,
                "music": {
                    "is_open": True,
                    "volume": 100
                },
                "effect": {
                    "is_open": True,
                    "volume": 100
                }
            }
        }
    }

    def __init__(self):
        self.config_files = {}
        if "config" not in os.listdir("."):
            os.mkdir("config")
            self.config_files["game_basic_config"] = {
                "json": open("config/game_basic.json", "w"),
                "binary": open("config/game_basic.bin", "wb")
            }
            self.config_files["game_basic_config"]["json"].write(json.dumps(self.DEFAULT["game_basic"]))
            self.config_files["game_basic_config"]["json"].close()
            self.config_files["game_basic_config"]["json"] = open("config/game_basic.json")
            jb_helper.serialize_json2bin(self.config_files["game_basic_config"]["binary"],
                                         self.config_files["game_basic_config"]["json"])
            self.config_files["game_basic_config"]["binary"].close()
            self.config_files["game_basic_config"]["json"].close()
            self.config = self.DEFAULT
        else:
            self.config_files["game_basic_config"] = {
                "json": open("config/game_basic.json"),
                "binary": open("config/game_basic.bin", "rb")
            }
            if jb_helper.is_file_changed(self.config_files["game_basic_config"]["binary"],
                                         self.config_files["game_basic_config"]["json"]):
                self.config_files["game_basic_config"]["binary"] = open("config/game_basic.bin", "wb")
                jb_helper.serialize_json2bin(self.config_files["game_basic_config"]["binary"],
                                             self.config_files["game_basic_config"]["json"])
                self.config_files["game_basic_config"]["binary"].close()
                self.config_files["game_basic_config"]["binary"] = open("config/game_basic.bin", "rb")
                self.config = jb_helper.get_bin_file_context(self.config_files["game_basic_config"]["binary"])
                self.config_files["game_basic_config"]["binary"].close()
                self.config_files["game_basic_config"]["json"].close()
            else:
                self.config = jb_helper.get_bin_file_context(self.config_files["game_basic_config"]["binary"])
                self.config_files["game_basic_config"]["binary"].close()
                self.config_files["game_basic_config"]["json"].close()
