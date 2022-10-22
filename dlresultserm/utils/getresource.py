import pkgutil
from pathlib import Path


def get_resource_content(relative_path):

    data = pkgutil.get_data(__name__, str(Path("..", relative_path)))
    if data is not None:
        return data.decode('utf-8')
    else:
        raise ValueError()
