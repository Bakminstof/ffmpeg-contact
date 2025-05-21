from pathlib import Path

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

__all__ = ("LoggingSettings",)


class LoggingSettings(BaseModel):
    model_config = ConfigDict(validate_default=True)

    version: int = 1
    disable_existing_loggers: bool = False
    encoding: str = "UTF-8"

    add_timestamp: bool = True
    add_logger_name: bool = True

    loglevel: str = "INFO"

    @field_validator("loglevel", mode="before")
    @classmethod
    def loglevel_validator(cls, value: str) -> str:
        return value.upper()

    log_format: str | None = None

    @field_validator("log_format", mode="before")
    @classmethod
    def log_format_validator(cls, value: str | None, info: ValidationInfo) -> str:
        if value:
            return value

        timestamp = " | %(asctime)s" if info.data.get("add_timestamp") else ""
        logger_name = " | %(name)s" if info.data.get("add_logger_name") else ""

        return f"%(levelname)s{timestamp}{logger_name} | %(message)s"

    log_datetime_format: str = "%Y-%m-%d %H:%M:%S"

    coloring_output: bool = True

    rotating_file_handler: bool = True
    logs_dir: Path | str = "logs"
    filename: str = "app.log"
    max_bytes: int = 10_485_760
    backup_count: int = 20

    @field_validator("logs_dir")
    @classmethod
    def logs_dir_validator(cls, value: str) -> Path:
        path = Path(value)

        if value.startswith("/") or value[1:3] == ":\\":
            directory = path

        else:
            directory = Path(__file__).parent.parent.parent / value

        if not directory.exists():
            directory.mkdir()

        return directory

    @field_validator("filename")
    @classmethod
    def filename_validator(cls, value: str, info: ValidationInfo) -> str:
        log_filename_path: Path = info.data["logs_dir"] / value
        return log_filename_path.absolute().as_posix()
