import asyncio
from pathlib import Path

from decryptor import decrypt_gamedata
from downloader import download_update, Platform, get_current_version
from xml_to_json import convert_gamedata


def rm_tree(path: Path):
    for child in path.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    path.rmdir()


async def main():
    platform = Platform.linux
    path = Path("out")

    version_path = path / "version.txt"

    version = get_current_version(platform)

    if version_path.exists():
        old_version = version_path.read_text()

        if version != old_version:
            print(f"Updating {old_version} -> {version}")
        else:
            print("Already completed")
            return

    await download_update(Platform.linux, version)
    version_path.write_text(version)

    print("Decrypt")
    decrypt_gamedata(path / "bin")

    print("Convert")
    convert_gamedata(path / "xml")

    print("Cleanup")
    rm_tree(path / "bin")
    rm_tree(path / "xml")


if __name__ == "__main__":
    asyncio.run(main())
