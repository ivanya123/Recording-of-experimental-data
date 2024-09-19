import matplotlib.pyplot as plt
import json


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

stage_data = [
    "Этап 1",
    "Этап 2",
    "Этап 3",
    "Этап 4",
    "Этап 5",
    "Этап 6",
    "Этап 7",
    "Этап 8",
    "Этап 9"
]



def add_coating(coating, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['coating'].append(coating)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def add_material(material, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['material'].append(material)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def delete_material(material, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['material'].remove(material)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def delete_coating(coating, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['coating'].remove(coating)
        data['coating_colors'].pop(coating)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def delete_stage(stage, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['stage'].remove(stage)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def add_tool(tool, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['tool'].append(tool)
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        update_coating_colors(file_name)

def add_stage(stage, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['stage'].append(stage)
        with open(file_name, 'w') as file:
            json.dump(data, file,ensure_ascii=False ,indent=4)


def get_material(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['material']

def get_coating(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['coating']

def get_tool(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['tool']


def get_stage(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['stage']

def update_coating_colors(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    coatings = data.get('coating', [])
    coating_colors = data.get('coating_colors', {})

    # Список возможных цветов
    possible_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Назначение цветов новым покрытиям
    for coating in coatings:
        if coating not in coating_colors:
            color = possible_colors[len(coating_colors) % len(possible_colors)]
            coating_colors[coating] = color

    # Обновляем словарь данных
    data['coating_colors'] = coating_colors

    # Записываем обновленные данные обратно в JSON-файл
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print('Обновлены цвета покрытий в JSON-файле.')

def get_coating_colors(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['coating_colors']

if __name__ == '__main__':
    update_coating_colors('data_constant.json')
