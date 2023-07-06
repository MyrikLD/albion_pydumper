import json
from pathlib import Path
from xml.etree import ElementTree


def spells_index(tree):
    result = []
    for item in tree:
        if item.tag == "colortag":
            continue

        uniquename = item.attrib["uniquename"]

        result.append(uniquename)

        if item.find("channelingspell"):
            result.append(f"{uniquename}_channeling")

        # TODO: Fix this
        if len(result) == 2000:
            for i in range(1):
                result.append("")

    # def assert_index(name, index):
    #     assert result.index(name) == index, f"{result.index(name)} != {index}"
    #
    # assert_index("PASSIVE_SPELLPOWER_CHANCE_DAGGER", 46)
    # assert_index("PASSIVE_ARMOR_INCREASED_AASPEED", 149)
    # assert_index("PASSIVE_ARMOR_CD_REDUCTION", 150)
    # assert_index("SUNDERARMOR2", 2066)
    # assert_index("THROWINGBLADES", 2075)
    # assert_index("EXECUTEDAGGER", 2093)
    # assert_index("DISEMBOWEL", 2098)
    # assert_index("RAPIERSTAB", 2102)
    # assert_index("LIFESTEALAURA", 2763)

    return result


def create_spells_index():
    in_file = Path("out/xml/spells.xml")
    tree = ElementTree.fromstring(in_file.read_text())
    index = spells_index(tree)
    Path("out/json/spells_index.json").write_text(json.dumps(index, indent=2))


if __name__ == "__main__":
    create_spells_index()
