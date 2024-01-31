from rich.console import Console
from rich.tree import Tree
from pathlib import Path


def list_directory_tree_with_rich(directory):
    console = Console()
    tree = Tree(f"📁 {directory.name}")

    def add_items(tree, path):
        for item in path.iterdir():
            if item.is_dir():
                branch = tree.add(f"📁 {item.name}")
                add_items(branch, item)
            else:
                tree.add(f"📄 {item.name}")

    add_items(tree, directory)
    console.print(tree)


directory_path = Path(".")
list_directory_tree_with_rich(directory_path)
