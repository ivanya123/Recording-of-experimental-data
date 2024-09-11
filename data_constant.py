material_data = [
    'ВТ18У',
    'ВТ41',
    "ХН50МВКТЮР",
    "ХН58МБЮД-ИД"
]

coating_data = [
    "AlTiCrN3+TiB2",
    "AlTiCrN3+TiB2",
    "AlTiN3",
    "AlTiN3+TiB2",
    "AlTiNCrN3",
    "TiB2",
    "nACRo",
    "nACRo+TiB2",
    "nACo3",
    "nACo3+TiB2",
    "Uncoating"
]

tool_data = [
    "Фреза 12",
    "Фреза 20"
]


import json

def add_coating(coating, file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        data['coating'].append(coating)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)


def add_material(material, file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        data['material'].append(material)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)


def delete_material(material, file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        data['material'].remove(material)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

def delete_coating(coating, file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        data['coating'].remove(coating)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

def add_tool(tool, file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        data['tool'].append(tool)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)

def get_material(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data['material']

def get_coating(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data['coating']

def get_tool(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data['tool']


if __name__ == '__main__':
    with open('data_constant.json', 'w') as file:
        dict_data = {
            'material': material_data,
            'coating': coating_data,
            "tool": tool_data
        }
        json.dump(dict_data, file, indent=4)
