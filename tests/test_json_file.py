import pytest
from pathlib import Path
from ooj.file import JsonFile
from ooj.objets import RootTree, Tree, Entry

# Базовый путь для тестов JSON файлов
BASE_PATH = Path('tests/files/test_json_files')

# Пример тестового дерева
test_tree = RootTree(
    Entry("key", "value"),
    Tree("tree",
        Entry("key1", "value1"),
        Entry("key2", "value2")
    )
)

class TestJsonFile:
    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown(self):
        """Создает необходимые папки перед каждым тестом и удаляет после."""
        BASE_PATH.mkdir(parents=True, exist_ok=True)
        yield
        for json_file in BASE_PATH.glob("*.json"):
            json_file.unlink()  # Удаляем все тестовые файлы после каждого теста

    @pytest.mark.parametrize(
        "fp, data",
        [
            (BASE_PATH / "test_write.json", {"name": "test", "age": 25}),
            (BASE_PATH / "test_write_tree.json", test_tree),
        ]
    )
    def test_write(self, fp: Path, data):
        file = JsonFile(fp)
        file.create_if_not_exists()
        
        file.write(data)
        file_data = file.read()

        if isinstance(data, RootTree):
            data = data.to_dict()
        
        assert file_data == data

    def test_create_if_not_exists(self):
        """Тестирование создания файла, если он не существует."""
        file_path = BASE_PATH / "test_create.json"
        json_file = JsonFile(file_path)

        json_file.create_if_not_exists()

        assert file_path.exists()

    def test_delete(self):
        """Тестирование удаления файла."""
        file_path = BASE_PATH / "test_delete.json"
        json_file = JsonFile(file_path)
        
        json_file.create_if_not_exists()
        assert file_path.exists()

        json_file.delete()
        assert not file_path.exists()

    def test_clear(self):
        """Тестирование очистки содержимого файла."""
        file_path = BASE_PATH / "test_clear.json"
        json_file = JsonFile(file_path)
        json_file.create_if_not_exists()

        json_file.write({"key": "value"})
        assert json_file.read() == {"key": "value"}

        json_file.clear()
        assert json_file.read() == {}

    @pytest.mark.parametrize(
        "key_s, value",
        [
            ("key1", "value1"),
            (["key2", "nested_key2"], "nested_value"),
        ]
    )
    def test_set_entry(self, key_s, value):
        """Тестирование установки значений по ключу."""
        file = JsonFile(BASE_PATH / "test_set_entry.json")
        file.create_if_not_exists()

        file.set_entry(key_s, value)
        assert file.get_entry(key_s) == value

    @pytest.mark.parametrize(
        "key_s, value",
        [
            ("key1", "value1"),
            (["key2", "nested_key2"], "nested_value"),
        ]
    )
    def test_del_entry(self, key_s, value):
        """Тестирование удаления значения по ключу."""
        file = JsonFile(BASE_PATH / "test_del_entry.json")
        file.create_if_not_exists()

        file.set_entry(key_s, value)
        assert file.get_entry(key_s) == value

        file.del_entry(key_s)
        with pytest.raises(KeyError):
            file.get_entry(key_s)

    def test_read_tree(self):
        """Тестирование чтения JSON в виде дерева."""
        file = JsonFile(BASE_PATH / "test_tree.json")
        file.create_if_not_exists()
        file.write(test_tree)

        root_tree = file.read_tree()
        assert root_tree == test_tree