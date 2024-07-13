from ooj.json_file import JsonFile


FILES_PATH = 'tests\\files\\intersect'


def test_intersect_dict():
    file = JsonFile(f'{FILES_PATH}\\1.json')

    file.intersect({"4": 4, "5": 5, "6": 6})


def test_intersect_file():
    file_1 = JsonFile(f'{FILES_PATH}\\1.json')
    file_2 = JsonFile(f'{FILES_PATH}\\2.json')

    file_1.intersect(file_2)