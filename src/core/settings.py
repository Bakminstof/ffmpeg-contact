from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

ENV_DIR = BASE_DIR / "env"


def get_abs_path(root: Path, value: str) -> Path:
    path = Path(value)

    if value.startswith("/") or value[1:3] == ":\\":
        abs_path = path

    else:
        abs_path = root / value

    return abs_path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="app.",
        env_file=(
            f"{ENV_DIR / '.env.template'}",
            f"{ENV_DIR / '.env'}",
        ),
        case_sensitive=False,
        arbitrary_types_allowed=True,
        env_nested_delimiter=".",
        env_file_encoding="UTF-8",
    )

    # ======================================|Main|====================================== #
    debug: bool = True

    default_encoding: str = "UTF-8"

    base_dir: Path = BASE_DIR

    source_list_filename: str = "list.txt"
    ignore: list[str] = [".gitkeep"]

    ffmpeg: Path = BASE_DIR.parent / "ffmpeg" / "bin" / "ffmpeg.exe"


settings = Settings()
