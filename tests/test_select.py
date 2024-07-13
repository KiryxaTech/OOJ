from ooj.json_file import JsonFile


FILES_PATH = 'tests\\files\\intersect'


def test_select():
    file = JsonFile(f'{FILES_PATH}\\1.json')

    print(file.select([range(0, 100)]))