import asyncio
import hashlib
from enum import Enum
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

import httpx
from httpx import AsyncClient


class Platform(str, Enum):
    linux = "linux"
    win32 = "win32"
    macosx = "macosx"
    android = "android"
    androidplaystore = "androidplaystore"
    ios = "ios"

    def __str__(self):
        return self.value


class ConcurrencyLimiter:
    def __init__(self, limit=4):
        self.sem = asyncio.Semaphore(limit)

    async def __call__(self, task):
        async with self.sem:
            return await task


async def download_file(
    client: AsyncClient, platform: Platform, version: str, file: dict
):
    path = Path(file["path"])

    new_file = Path("out/bin") / path.with_name(path.stem).relative_to(
        "Albion-Online_Data/StreamingAssets/GameData"
    )

    if new_file.exists():
        old_md5 = md5(new_file)
        new_md5 = file["md5"]
        if old_md5 == new_md5:
            print(f"Skip: {path}")
            return
    else:
        new_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Download: {path}")

    r = await client.get(
        f"https://live.albiononline.com/autoupdate/perfileupdate/{platform}_{version}/{path}"
    )

    with ZipFile(BytesIO(r.read())) as zip_ref:
        zip_ref.extract(new_file.name, new_file.parent)


def md5(file: Path):
    hash_md5 = hashlib.md5()
    hash_md5.update(file.read_bytes())
    return hash_md5.hexdigest()


def get_current_version(platform: Platform) -> str:
    r = httpx.get("https://live.albiononline.com/autoupdate/manifest.xml")
    tree = ElementTree.fromstring(r.text)
    version = tree.find(f"albiononline/{platform}/fullinstall").attrib["version"]

    return version


def get_file_list(platform: Platform, version: str) -> list[dict]:
    r = httpx.get(
        f"https://live.albiononline.com/autoupdate/perfileupdate/{platform}_{version}/toc_{platform}.xml"
    )
    tree = ElementTree.fromstring(r.text)
    files = [i.attrib for i in tree]

    return files


async def download_update(platform: Platform, version: str):
    files = get_file_list(platform, version)

    tasks = []
    limiter = ConcurrencyLimiter(8)
    async with AsyncClient() as c:
        for file in files:
            path = Path(file["path"])

            if not path.is_relative_to("Albion-Online_Data/StreamingAssets/GameData"):
                continue

            if len(path.suffixes) != 2 or path.suffixes[-2] != ".bin":
                continue

            if path.name.startswith("profanity_"):
                continue

            task = download_file(c, platform, version, file)

            tasks.append(limiter(task))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(download_update(Platform.linux))
