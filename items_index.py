import json
from pathlib import Path
from xml.etree import ElementTree


def items_index(tree):
    result = ["NULL"]

    for item in tree:
        if item.tag == "shopcategories":
            continue

        uniquename = item.attrib["uniquename"]
        enchantmentlevel = item.attrib.get("enchantmentlevel")

        if enchantmentlevel and enchantmentlevel != "0":
            # result[index] = f"{uniquename}@{enchantmentlevel}"
            # index += 1

            result.append(f"{uniquename}@{enchantmentlevel}")
        elif enchantments := item.find("enchantments") or []:
            # result[index] = uniquename
            # index += 1

            result.append(f"{uniquename}")
            for i in enchantments:
                # result[index] = f"{uniquename}@{i.attrib['enchantmentlevel']}"
                # index += 1

                result.append(f"{uniquename}@{i.attrib['enchantmentlevel']}")
        else:
            # result[index] = uniquename
            # index += 1

            result.append(f"{uniquename}")

    return result


def create_items_index():
    in_file = Path("out/xml/items.xml")
    tree = ElementTree.fromstring(in_file.read_text())
    index = items_index(tree)
    Path("out/json/items_index.json").write_text(json.dumps(index, indent=2))


if __name__ == "__main__":
    create_items_index()
