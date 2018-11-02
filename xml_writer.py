import xmltodict
import json

config_file_path = 'D:\\FileZilla Server\\FileZilla Server.xml'
user_template_path = 'user_template.xml'


with open(config_file_path) as file:
    config_dict = xmltodict.parse(file.read())

with open(user_template_path) as file:
    user_dict = xmltodict.parse(file.read())

print(json.dumps(config_dict, indent=4))
convertXml = xmltodict.unparse(config_dict)


with open(config_file_path, mode='w') as file:
    file.write(convertXml)
