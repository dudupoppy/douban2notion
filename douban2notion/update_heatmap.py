import argparse
import os
import shutil
import time
from douban2notion.notion_helper import NotionHelper

def move_and_rename_file(type):
    source_path = os.path.join("./OUT_FOLDER", 'notion.svg')
    artifact_root = os.getenv(
        "NOTIONHUB_ARTIFACT_ROOT",
        os.path.abspath(".notionhub-artifacts/douban"),
    )
    target_dir = os.path.join(artifact_root, type)
    os.makedirs(target_dir, exist_ok=True)
    timestamp = int(time.time())
    new_filename = f"{timestamp}.svg"
    target_path = os.path.join(target_dir, new_filename)
    shutil.move(source_path, target_path)
    return new_filename
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    options = parser.parse_args()
    type = options.type
    if type not in {"movie", "book"}:
        raise ValueError("免费版只支持 movie 和 book 热力图")
    notion_helper = NotionHelper(type)
    filename = move_and_rename_file(type)
    if filename:
        repository = os.environ["REPOSITORY"]
        branch = os.getenv("ARTIFACT_BRANCH", "main")
        relative_root = os.getenv(
            "NOTIONHUB_ARTIFACT_PATH",
            ".notionhub-artifacts/douban",
        ).strip("/")
        heatmap_url = (
            f"https://raw.githubusercontent.com/{repository}/{branch}/"
            f"{relative_root}/{type}/{filename}"
        )
        if notion_helper.heatmap_block_id:
            notion_helper.update_heatmap(
                block_id=notion_helper.heatmap_block_id, url=heatmap_url
            )
if __name__ == "__main__":
    main()
