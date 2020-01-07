import json

#consumes: path to jsonfile as String
#returns: dict
def get_config(file_name):
    config_file = open(file_name, "r", encoding="utf-8")
    config = json.load(config_file)
    config_file.close()
    return config


#print(get_config("../resources/SerialConfig.json")["port"])

