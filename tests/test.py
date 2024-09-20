from ooj.json_objects import RootTree, Tree, Entry
from ooj.json_file import JsonFile


def test_tree():
    file = JsonFile('test.json')
    file.create_if_not_exists()

    tree = RootTree(
        Tree('settings',
            Entry('theme', 'dark'),
            Entry('accent_color', 'nebula'),
            Tree('log-in',
                Entry('email', None),
                Entry('password', None)
            )
        ),
        Entry('id', '1039294912047021')
    )

    file.write(tree)
    print(file.read())

    assert tree.to_dict() == file.read()

def test_converter():
    file = JsonFile('test.json')
    file.create_if_not_exists()

    tree = RootTree(
        Tree('settings',
            Entry('theme', 'dark'),
            Entry('accent_color', 'nebula'),
            Tree('log-in',
                Entry('email', None),
                Entry('password', None)
            )
        ),
        Entry('id', '1039294912047021')
    )

    file.write(tree)

    print("Written Tree:", tree.to_dict())
    print("Read Tree:", file.read_tree().to_dict())

    assert tree.to_dict() == file.read_tree().to_dict()