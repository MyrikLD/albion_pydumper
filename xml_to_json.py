import json
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def parse_tree(element: Element):
    item = {"tag": element.tag}

    for k, v in element.attrib.items():
        item[f"@{k}"] = v

    obj = defaultdict(list)

    for sub in element:
        i = parse_tree(sub)
        obj[i.pop("tag")].append(i)

    item.update(obj)

    return item


def decode(in_file: Path, out_file: Path):
    assert in_file.is_file()
    assert in_file.suffix == ".xml"
    assert out_file.suffix == ".json"

    tree = ElementTree.fromstring(in_file.read_text())
    data = parse_tree(tree)
    out_file.write_text(json.dumps(data, indent=2))


def convert_gamedata(dir_path: Path, start=None):
    start = start or dir_path

    for path in dir_path.iterdir():
        if path.is_file():
            new_path = (
                Path.cwd()
                / "out"
                / "json"
                / path.relative_to(start).with_suffix(".json")
            )
            new_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                decode(path, new_path)
            except Exception:
                print(f"Exception in {path}")
        else:
            convert_gamedata(path, start=start)


def main():
    convert_gamedata(Path("out") / "xml")


if __name__ == "__main__":
    main()
