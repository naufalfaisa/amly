import sys
from colorama import init, Fore, Style

init(autoreset=True)

class Logger:
    def info(self, log, exit=0):
        print(f"{log}")
        if exit == 1:
            sys.exit()

    def warning(self, log, exit=0):
        print(f"{Fore.YELLOW + Style.BRIGHT}[WARNING]{Style.RESET_ALL} {log}")
        if exit == 1:
            sys.exit()

    def error(self, log, exit=0):
        print(f"{Fore.RED + Style.BRIGHT}[ERROR]{Style.RESET_ALL} {log}")
        if exit == 1:
            sys.exit()

    def done(self, log, exit=0):
        print(f"{Fore.GREEN + Style.BRIGHT}[DONE]{Style.RESET_ALL} {log}")
        if exit == 1:
            sys.exit()

logger = Logger()
