import json
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


def parse_tree(d: Element):
    item = {"tag": d.tag}

    for k, v in d.attrib.items():
        item[f"@{k}"] = v

    sub = [parse_tree(i) for i in d]
    d = defaultdict(list)
    for i in sub:
        d[i.pop("tag")].append(i)

    item.update(d)

    return item


def decode(in_file: Path, out_file: Path):
    tree = ElementTree.fromstring(in_file.read_text())
    data = parse_tree(tree)
    out_file.write_text(json.dumps(data, indent=2))


def parse_gamedata(dir_path: Path, start=None):
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
            parse_gamedata(path, start=start)


def main():
    parse_gamedata(Path("out") / "xml")


if __name__ == "__main__":
    main()
