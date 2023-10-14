import logging
import argparse

LOG = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(
        description="Script to convert transactions extract into loadable format via LOL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--first_name",
        type=str,
        metavar="",
        help="First Name",
    )

    parser.add_argument(
        "-l",
        "--last_name",
        type=str,
        metavar="",
        help="Last Name",
    )
    return parser.parse_args()

def get_name(firstname: str, lastname: str):
    if firstname == "David":
        LOG.info(f"Hello World: You entered {firstname} {lastname}")
        return firstname, lastname
    else:
        raise ValueError(f"The fistname: {firstname} is not accepted.")

if __name__ == "__main__":
    args = get_args()
    get_name(args.first_name, args.last_name)