from pathlib import Path

from pydantic import BaseModel


class Args(BaseModel):
    debug: bool = False

    target_extension: str

    source: Path
    destination: Path | None = None

    result_filename: str | None = None
