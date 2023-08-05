from . import versioning


def main() -> None:
    """Program entry point function."""
    try:
        print(versioning.get_version())
    except Exception as exp:
        exit(exp)


if __name__ == '__main__':
    main()
