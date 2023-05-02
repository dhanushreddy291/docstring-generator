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
        """
        Initializes an object of the class with the given file path. Raises a FileNotFoundError if the file does not exist. The path and type of the file are stored as attributes of the object.
        """
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        self.path = path
        self.type = self.find_type()

    def find_type(self) -> str:
        """
        This function determines the type of the file based on its extension. If the type cannot be recognized, an Exception is raised. The function returns the type of the file, which is either "image" or "video". If the type is not supported, a ValueError is raised.
        """
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
        """
        Initializes an object of the class with the given overlay file, position and offset. The overlay file and position are stored as attributes of the object. If no offset is provided, the default offset for the given position is used. The offset is also stored as an attribute of the object.
        """
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
    """
    Applies the given watermark to the given file using FFmpeg. The output file path is optional, and if not provided, it is generated based on the input file path. The frame rate and preset for the output file can also be specified. If the output file already exists and overwrite is set to True, it is deleted before the new file is generated. The function returns the path of the output file.
    """
    if not output_file:
        if file.type == "video":
            output_file = f"watered_{file.path}.gif"
        else:
            output_file = f"watered_{file.path}"

    cmd = [
        "ffmpeg",
        "-i",
        file.path,
        "-i",
        wtm.overlay,
        "-an",  # comment to enable audio
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
