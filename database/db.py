"""
"""
import json
from pathlib import Path
from slugify import slugify


class VideoDatabase:
    def __init__(self) -> None:
        self.file = Path("database/video.json")
        if self.file.stat().st_size == 0:
            with open(self.file, "w") as f:
                json.dump([], f, indent=4)

    def list(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def get(self, oid):
        with open(self.file) as f:
            videos = json.load(f)
            for video in videos:
                if video.get("oid") == oid:
                    return video

    def add(self, oid, title, prefix, suffix):
        with open(self.file, "r") as f:
            videos = json.load(f)
        videos.append(
            {
                "oid": oid,
                "title": title,
                "prefix": prefix,
                "og_file": f"og{suffix}",
                "manifest": f"og.mpd",
            }
        )
        with open(self.file, "w") as f:
            json.dump(videos, f, indent=4)

    def delete(self, oid):
        with open(self.file, "r") as f:
            videos = json.load(f)
        videos = [video for video in videos if video.get("oid") != oid]
        with open(self.file, "w") as f:
            json.dump(videos, f, indent=4)
