from pathlib import Path


def list_directory_tree_with_pathlib(directory, indent=0):
    for item in directory.iterdir():
        if item.is_file():
            print(f"{' ' * indent}File: {item.name}")
        elif item.is_dir():
            print(f"{' ' * indent}Directory: {item.name}")
            list_directory_tree_with_pathlib(item, indent + 4)


directory_path = Path(".")
list_directory_tree_with_pathlib(directory_path)
