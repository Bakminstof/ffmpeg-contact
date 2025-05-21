from logging import INFO, WARNING, getLogger
from subprocess import PIPE, Popen
from typing import IO, AnyStr

logger = getLogger(__name__)


def run_process(args: list[str], title: str, encoding: str) -> None:
    logger.info("Start process `%s`: command=%s", title, " ".join(args))

    process = Popen(
        args=args,
        stderr=PIPE,
        stdout=PIPE,
        shell=True,
        text=True,
        encoding=encoding,
    )

    while process.poll() is None:
        __capture_output(process.stderr)

    if process.returncode != 0:
        logger.error("Process `%s` exited with code: %s", title, process.returncode)
    else:
        logger.info("Process `%s` exited successfully", title)


def __capture_output(data: IO[AnyStr], loglevel: int = INFO) -> None:
    for line in data:
        if loglevel == INFO:
            logger.info(line.strip())
        elif loglevel == WARNING:
            logger.warning(line.strip())
        else:
            continue
