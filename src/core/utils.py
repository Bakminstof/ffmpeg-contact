from argparse import ArgumentParser, BooleanOptionalAction
from logging import getLogger
from pathlib import Path
from re import match, search

from core.models import Args
from core.process import run_process
from core.settings import settings
from logging_settings.utils import make_logging_settings, setup_logging

logger = getLogger(__name__)


def get_args() -> Args:
    parser = ArgumentParser()

    parser.add_argument(
        "--debug",
        action=BooleanOptionalAction,
        default=False,
        required=False,
    )
    parser.add_argument(
        "--target_extension",
        "-te",
        type=str,
        default="3gp",
        required=False,
    )
    parser.add_argument(
        "--source",
        "-s",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--destination",
        "-d",
        type=Path,
        default=None,
        required=False,
    )
    parser.add_argument(
        "--result_filename",
        "-n",
        type=str,
        default=None,
        required=False,
    )

    return Args(**vars(parser.parse_args()))


def startup(args: Args) -> None:
    logging_settings = make_logging_settings(
        loglevel="DEBUG" if args.debug else "INFO",
        filename="ffmpeg-contact.log",
    )
    setup_logging(logging_settings)

    settings.debug = args.debug


def contact_files(
    source: Path,
    source_list_file: Path,
    target_suffix: str,
    destination: Path | None = None,
    result_filename: str | None = None,
    encoding: str = settings.default_encoding,
    ffmpeg: Path = settings.ffmpeg,
) -> Path:
    if destination is None:
        destination = source

    if result_filename is None:
        result_filename = f"{source.name}.{target_suffix}"

    result_file = destination / result_filename

    if result_file.exists():
        result_file.unlink()

    ffmpeg_args = [
        ffmpeg.absolute().as_posix(),
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        source_list_file.absolute().as_posix(),
        "-c:v",
        "copy",
        result_file.absolute().as_posix(),
    ]

    run_process(ffmpeg_args, "FFMpeg", encoding)

    return result_file


def make_source_list_file(
    source: Path,
    source_files: list[Path],
    source_list_filename: str = settings.source_list_filename,
    encoding: str = settings.default_encoding,
) -> Path:
    source_list_file_path = source / source_list_filename
    lines = []

    for source_file in source_files:
        line = f"file '{source_file.name}'\n"

        lines.append(line)

    with source_list_file_path.open(mode="w", encoding=encoding) as source_list_file:
        source_list_file.writelines(lines)

    logger.info(
        "Written source list file: %s",
        source_list_file_path.absolute().as_posix(),
    )

    return source_list_file_path


def get_source_files(
    source: Path,
    target_suffix: str,
    ignore: list[str] = settings.ignore,
) -> list[Path]:
    if source.name in ignore:
        return []

    if not source.is_dir():
        logger.warning("%s is not a directory", source)
        return []

    data = []

    for item in source.iterdir():
        if item.is_dir():
            continue

        if match(
            rf"\d{{1,3}}_\d{{4}}-\d{{2}}-\d{{2}}_\d{{6}}\.{target_suffix}",
            item.name,
        ):
            data.append(item)

    logger.info("Got target files: %d", len(data))
    logger.debug(
        "Target files: %s",
        [path.absolute().as_posix() for path in data],
    )

    return sort(data)


def sort(data: list[Path]) -> list[Path]:
    keys_data = {}

    for item in data:
        number_str = search(r"\d+(?=_)", item.name)

        if number_str is None:
            logger.warning("Can't parse item number: item=%s", item.name)
            continue

        number = int(number_str.group())

        keys_data[number] = item

    sorted_keys = sorted(keys_data)

    return [keys_data[number] for number in sorted_keys]


def start(
    source: Path,
    target_suffix: str,
    destination: Path | None = None,
    result_filename: str | None = None,
) -> None:
    source_files = get_source_files(source, target_suffix)

    if not source_files:
        return

    source_list_file = make_source_list_file(source, source_files)
    contact_files(source, source_list_file, target_suffix, destination, result_filename)
