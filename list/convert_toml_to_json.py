import os
import toml
import json
import hashlib
from pathlib import Path

# 定义扩展根目录（包含多个扩展子目录）
EXTENSIONS_DIR = Path("../addon_release")
# 生成的 JSON 清单路径
INDEX_JSON_PATH = Path("index.json")


def convert_toml_to_json():
    manifest_data = []
    for ext_dir in EXTENSIONS_DIR.glob("*"):
        toml_file = ext_dir / "blender_manifest.toml"
        if not toml_file.exists():
            continue  # 跳过无 TOML 文件的目录

        try:
            # 读取 TOML 元数据
            tomd = toml.load(toml_file)
        except Exception as e:
            print(f"加载 {toml_file} 文件时出现异常：{e}")
            continue

        # 获取 ZIP 文件信息（假设 ZIP 与 TOML 同名）
        zip_path = ext_dir / f"{tomd['id']}.zip"
        if not zip_path.exists():
            raise FileNotFoundError(f"ZIP file not found for {tomd['id']}")

        # 计算文件大小和哈希值
        zip_size = os.path.getsize(zip_path)
        with open(zip_path, "rb") as f:
            zip_hash = hashlib.sha256(f.read()).hexdigest()

        # 构建 JSON 条目
        json_entry = {
            "schema_version": tomd.get("schema_version", "1.0.0"),
            "id": tomd["id"],
            "name": tomd["name"],
            "tagline": tomd.get("tagline", ""),
            "version": tomd["version"],
            "type": tomd["type"],
            "maintainer": tomd["maintainer"],
            "license": tomd["license"],
            "blender_version_min": tomd["blender_version_min"],
            "blender_version_max": tomd.get("blender_version_max", ""),
            "website": tomd.get("website", ""),
            "tags": tomd.get("tags", []),
            "archive_url": f"./addon_release/{tomd['id']}/{tomd['id']}.zip",
            "archive_size": zip_size,
            "archive_hash": f"sha256:{zip_hash}"
        }
        manifest_data.append(json_entry)

    # 生成最终的 JSON 清单
    final_manifest = {
        "version": "v1",
        "blocklist": [],
        "data": manifest_data
    }
    with open(INDEX_JSON_PATH, "w") as f:
        json.dump(final_manifest, f, indent=2)


def move_file(source_file, target_path):
    try:
        # 移动文件
        source_file.rename(target_path / source_file.name)
        print(f"文件 {source_file.name} 已成功移动到 {target_path}")
    except Exception as e:
        print(f"移动文件时出现错误：{e}")


if __name__ == "__main__":
    convert_toml_to_json()
    print(f"JSON manifest generated at {INDEX_JSON_PATH}")

    # 源文件路径
    source_file = Path("D:/ART实验库/gittest/Blender-for-AART/list/index.json")
    # 目标路径（最外层文件夹路径）
    target_path = Path("D:/ART实验库/gittest/Blender-for-AART")
    # 移动文件
    move_file(source_file, target_path)
