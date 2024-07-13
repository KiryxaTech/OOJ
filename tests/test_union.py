from ooj.file import JsonFile

FILES_PATH = 'tests\\files\\union'

def test_union_dict():
    file = JsonFile(f'{FILES_PATH}\\1.json')

    file.union({"4": 4, "5": 5, "6": 6})

def test_union_file():
    file_1 = JsonFile(f'{FILES_PATH}\\1.json')
    file_2 = JsonFile(f'{FILES_PATH}\\2.json')

    file_1.union(file_2)