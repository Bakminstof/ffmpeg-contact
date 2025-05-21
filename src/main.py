from core.utils import get_args, start, startup


def main() -> None:
    args = get_args()

    startup(args)

    start(args.source, args.target_extension, args.destination, args.result_filename)


if __name__ == "__main__":
    main()
