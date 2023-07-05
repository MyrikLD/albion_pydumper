import gzip
from pathlib import Path

from Crypto.Cipher import DES

key = bytes([0x30, 0xEF, 0x72, 0x47, 0x42, 0xF2, 0x04, 0x32])
IV = bytes([0x0E, 0xA6, 0xDC, 0x89, 0xDB, 0xED, 0xDC, 0x4F])


def decode(in_file: Path, out_file: Path):
    assert in_file.is_file()
    assert in_file.suffix == ".bin"
    assert out_file.suffix == ".xml"

    data = in_file.read_bytes()

    crypter = DES.new(key=key, mode=DES.MODE_CBC, IV=IV)

    decrypted = crypter.decrypt(data)
    decrypted = decrypted.rstrip(decrypted[-1:])
    decompressed = gzip.decompress(decrypted)

    out_file.write_bytes(decompressed)


def decrypt_gamedata(dir_path: Path, start=None):
    start = start or dir_path

    for path in dir_path.iterdir():
        if path.is_file():
            if path.name.startswith("profanity_"):
                continue
            new_path = (
                Path.cwd() / "out" / "xml" / path.relative_to(start).with_suffix(".xml")
            )
            new_path.parent.mkdir(parents=True, exist_ok=True)
            decode(path, new_path)
        else:
            decrypt_gamedata(path, start=start)


# def parse_game_folder(game_folder: Path):
#     parse_gamedata(
#         game_folder / "game_x64" / "Albion-Online_Data" / "StreamingAssets" / "GameData"
#     )


def main():
    decrypt_gamedata(Path("out/bin"))


if __name__ == "__main__":
    main()
