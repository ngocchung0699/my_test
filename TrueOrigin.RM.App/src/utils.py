from pathlib import Path

def get_project_root() -> Path:
    return str(Path(__file__).parent.parent)

if __name__ == '__main__':
    root = get_project_root()
    print(root)