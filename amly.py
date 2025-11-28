import argparse
from src.logger import logger
from colorama import init, Fore, Style
from src.handler import handler

init(autoreset=True)

LOGO = f"\n{Fore.RED + Style.BRIGHT}────── AMLY Downloader ──────{Style.RESET_ALL}"

ASCII_ART = f"""
{Style.BRIGHT}⣿⣿⣿⡷⠊⡢⡹⣦⡑⢂⢕⢂⢕⢂⢕⢂⠕⠔⠌⠝⠛⠶⠶⢶⣦⣄⢂⢕⢂⢕
⣿⣿⠏⣠⣾⣦⡐⢌⢿⣷⣦⣅⡑⠕⠡⠐⢿⠿⣛⠟⠛⠛⠛⠛⠡⢷⡈⢂⢕⢂
⠟⣡⣾⣿⣿⣿⣿⣦⣑⠝⢿⣿⣿⣿⣿⣿⡵⢁⣤⣶⣶⣿⢿⢿⢿⡟⢻⣤⢑⢂
⣾⣿⣿⡿⢟⣛⣻⣿⣿⣿⣦⣬⣙⣻⣿⣿⣷⣿⣿⢟⢝⢕⢕⢕⢕⢽⣿⣿⣷⣔
⣿⣿⠵⠚⠉⢀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⢕⢕⢕⢕⢕⢕⣽⣿⣿⣿⣿
⢷⣂⣠⣴⣾⡿⡿⡻⡻⣿⣿⣴⣿⣿⣿⣿⣿⣿⣷⣵⣵⣵⣷⣿⣿⣿⣿⣿⣿⡿
⢌⠻⣿⡿⡫⡪⡪⡪⡪⣺⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃
⠣⡁⠹⡪⡪⡪⡪⣪⣾⣿⣿⣿⣿⠋⠐⢉⢍⢄⢌⠻⣿⣿⣿⣿⣿⣿⣿⣿⠏⠈
⡣⡘⢄⠙⣾⣾⣾⣿⣿⣿⣿⣿⣿⡀⢐⢕⢕⢕⢕⢕⡘⣿⣿⣿⣿⣿⣿⠏⠠⠈
⠌⢊⢂⢣⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢕⢕⢕⢕⢕⢅⣿⣿⣿⣿⡿⢋⢜⠠⠈
"""

def main():
    """
    Main entry point for the AMLY Downloader.
    Parses command-line arguments and calls the appropriate handler.
    """
    print(LOGO)
    print(ASCII_ART)

    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="Command line tool to download lyrics from Apple Music"
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s v1.0.0'
    )
    parser.add_argument(
        '-s', '--sync',
        help="Save timecode's in 00:00.000 format (three ms points)",
        action="store_true"
    )
    parser.add_argument(
        '-r', '--romaji',
        help="Convert Japanese lyrics to Romaji (requires MeCab/Cutlet)",
        action="store_true"
    )
    parser.add_argument(
        'urls',
        help="Apple Music URLs for albums or songs",
        type=str,
        nargs='*'
    )
    args = parser.parse_args()

    if not any([args.urls, args.sync]):
        logger.warning("Don't run this by double-clicking the exe. Use command line arguments instead!")
        parser.print_usage()
        input("Enter to exit...")
        return
    
    # Execute the main handler with the parsed arguments
    handler(args)

if __name__ == "__main__":
    main()

