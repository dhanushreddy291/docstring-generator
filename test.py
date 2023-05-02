import os
from enum import Enum
from mimetypes import guess_type
import subprocess


class Position(str, Enum):
    top_left = "top_left"
    top_right = "top_right"
    centre = "centre"
    bottom_left = "bottom_left"
    bottom_right = "bottom_right"


offset_map = {
    "top_left": "10:10",
    "top_right": "W-w-10:10",
    "centre": "(W-w)/2:(H-h)/2",
    "bottom_left": "10:H-h-10",
    "bottom_right": "W-w-10:H-h-10",
}


class File:
    def __init__(self, path: str) -> None:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        self.path = path
        self.type = self.find_type()

    def find_type(self) -> str:
        _type = guess_type(self.path)[0]
        if not _type:
            raise Exception(f"File type cant be recognized")

        _type = _type.split("/")[0]
        if _type in ["image", "video"]:
            return _type
        else:
            raise ValueError(f"Type {_type} is not supported.")


class Watermark:
    def __init__(
        self,
        overlay: File,
        pos: Position = Position.centre,
        offset: str = "",
    ) -> None:
        self.overlay = overlay
        self.pos = pos
        if not offset:
            offset = offset_map.get(self.pos)
        self.offset = offset


def apply_watermark(
    file: File,
    wtm: Watermark,
    output_file: str = "",
    frame_rate: int = 15,
    preset: str = "ultrafast",
    overwrite: bool = True,
) -> str:
    if not output_file:
        if file.type == 'video':
            output_file = f"watered_{file.path}.gif"
        else:
            output_file = f"watered_{file.path}"

    cmd = [
        "ffmpeg",
        "-i",
        file.path,
        "-i",
        wtm.overlay,
        "-an", # comment to enable audio
        "-dn",
        "-sn",
        "-r",
        str(frame_rate),
        "-preset",
        preset,
        "-crf",
        str(30),
        "-movflags",
        "+faststart",
        "-tune",
        "zerolatency",
        "-tune",
        "fastdecode",
        "-filter_complex",
        f"overlay={wtm.offset}",
        output_file,
    ]

    if os.path.isfile(output_file) and overwrite:
        os.remove(output_file)

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_file