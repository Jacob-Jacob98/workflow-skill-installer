"""Install the two Codex skills. Run with Python 3.8 or newer."""
import getpass
import hashlib
import io
import os
import secrets
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

ENDPOINT = "https://workflow-install-gateway.kamalbarmankamalbarman339.workers.dev/redeem"
SHA256 = "5623c5cfb30c43beb21c014f9de78fb9e5db9f4806ce5bd50164229738e8d666"
SKILLS = ("image-prompt-replication", "wedding-music-workflow")


def download(code):
    headers = {"X-Install-Code": code, "X-Install-Claim": secrets.token_hex(16),
               "User-Agent": "WorkflowSkillInstaller/1.0 (+https://github.com/Jacob-Jacob98/workflow-skill-installer)"}
    request = urllib.request.Request(ENDPOINT, data=b"", headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() == SHA256:
                return data
            raise ValueError("安装包校验失败。")
        except urllib.error.HTTPError as error:
            if error.code == 403 and error.read(100) in (b"Invalid code", b"Expired, used or invalid code"):
                raise ValueError("安装码无效、已过期或已使用。") from error
            if error.code < 500 or attempt == 2:
                raise
        except OSError:
            if attempt == 2:
                raise
        time.sleep(1)


def install():
    root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "skills"
    root.mkdir(parents=True, exist_ok=True)
    missing = [name for name in SKILLS if not (root / name).exists()]
    if not missing:
        print("两个技能目录均已存在，已保留本地版本。")
        return
    with tempfile.TemporaryDirectory(dir=root) as tmp:
        data = download(getpass.getpass("请输入安装码（输入时隐藏）: ").strip())
        with zipfile.ZipFile(io.BytesIO(data)) as bundle:
            for item in bundle.infolist():
                path = PurePosixPath(item.filename)
                if path.parts[0] not in SKILLS or ".." in path.parts or "\\" in item.filename:
                    raise ValueError("安装包路径无效。")
            bundle.extractall(tmp)
        for name in missing:
            if not (Path(tmp) / name / "SKILL.md").is_file():
                raise ValueError("安装包缺少技能说明。")
        for name in missing:
            for attempt in range(8):
                try:
                    (Path(tmp) / name).rename(root / name)
                    break
                except PermissionError:
                    if attempt == 7:
                        raise
                    time.sleep(0.15 * (attempt + 1))
            print("已安装", name)
    print("请重启 Codex 加载技能。")


if __name__ == "__main__":
    try:
        install()
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        sys.exit(str(error))
