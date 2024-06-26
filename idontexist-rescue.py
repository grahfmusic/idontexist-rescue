#!/usr/bin/env python3

import os
import time
import subprocess
import datetime
import tarfile
import shutil
from pathlib import Path
from tqdm import tqdm
import argparse
import sys
from art import text2art
from termcolor import colored
import colorama
from colorama import init, Fore, Style

# Initialize colorama
colorama.init()

# Define backup paths
backup_paths = {
    "jellyfin": ["/var/lib/jellyfin", "/etc/jellyfin", "/usr/share/jellyfin"],
    "sonarr": ["/var/lib/sonarr"],
    "lidarr": ["/var/lib/lidarr"],
    "radarr": ["/var/lib/radarr"],
    "jellyseerr": ["/var/lib/jellyseerr"],
    "jackett": ["/var/lib/jackett"],
    "nginx": ["/etc/nginx"],
}

# Get current working directory
cwd = os.getcwd()


def print_header():
    os.system("clear")
    """Print the script header using text2art."""
    header = text2art("- idontexist-rescue -", font="tarty4")
    print(colored(header, "cyan"))
    print(colored("Version 1.0 // Coded by Grahf // github.com/grahfmusic\n", "green"))


def check_sudo(verbose):
    """Check if the script is run as root, if not re-execute with sudo."""
    if os.geteuid() != 0:
        print(colored(":: Requires sudo. Re-running with sudo...", "yellow"))
        if verbose:
            print(
                colored(f":: Sudo Command: sudo python3 {' '.join(sys.argv)}", "cyan")
            )
        try:
            os.execvp("sudo", ["sudo", "python3"] + sys.argv)
        except Exception as e:
            print(colored(f":: Sudo Execution Failed: {e}", "red"))
        sys.exit(1)


def run_command_with_progress(command, verbose):
    """Run a shell command and handle real-time output."""
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    total_bytes = 0
    term_width = shutil.get_terminal_size().columns
    progress_bar_length = 50
    start_time = time.time()

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            # Remove the "to " or "from " reminder text from the output
            output = output.replace("to ", "").replace("from ", "")
            total_bytes += len(output)

            # Calculate progress
            progress = total_bytes
            total = None  # Use None if total size is unknown
            percent = progress / total if total else 0
            elapsed = time.time() - start_time

            # Build the progress bar
            filled_length = int(progress_bar_length * percent)
            progress_bar = "█" * filled_length + "-" * (
                progress_bar_length - filled_length
            )

            # Create a color gradient for the text
            text_color = Fore.BLUE + Style.BRIGHT
            text_color_end = Fore.WHITE + Style.BRIGHT
            text_gradient = [
                text_color
                + chr(
                    int(
                        i
                        * (ord(text_color_end[-1]) - ord(text_color[-1]))
                        / progress_bar_length
                    )
                    + ord(text_color[-1])
                )
                + Style.RESET_ALL
                for i in range(filled_length)
            ]
            text_gradient += [
                Fore.WHITE + Style.BRIGHT + "-" + Style.RESET_ALL
                for _ in range(progress_bar_length - filled_length)
            ]

            # Add the color gradient to the progress bar
            progress_bar = "".join(text_gradient)

            # Add different colors for the '::' separators
            separator_colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN]
            separator_color_index = int(percent * len(separator_colors))
            separator = separator_colors[separator_color_index] + "::" + Style.RESET_ALL

            progress_bar = f"{separator} [{progress_bar}] {progress}/{total if total else '?'} [{elapsed:.2f}s]"

            # Print the progress bar on the same line
            print(f"\r{progress_bar}", end="", flush=True)

            if verbose:
                print(output.strip(), end="\r", flush=True)
            else:
                print(end="\r", flush=True)

            process.stdout.close()
            process.stderr.close()
            print()  # Print a newline after the progress bar
            return process.returncode


#!/usr/bin/env python3

import os
import time
import subprocess
import datetime
import tarfile
import shutil
from pathlib import Path
from tqdm import tqdm
import argparse
import sys
from art import text2art
from termcolor import colored
import colorama
from colorama import init, Fore, Style

# Initialize colorama
colorama.init()

# Define backup paths
backup_paths = {
    "jellyfin": ["/var/lib/jellyfin", "/etc/jellyfin", "/usr/share/jellyfin"],
    "sonarr": ["/var/lib/sonarr"],
    "lidarr": ["/var/lib/lidarr"],
    "radarr": ["/var/lib/radarr"],
    "jellyseerr": ["/var/lib/jellyseerr"],
    "jackett": ["/var/lib/jackett"],
    "nginx": ["/etc/nginx"],
}

# Get current working directory
cwd = os.getcwd()


def print_header():
    os.system("clear")
    """Print the script header using text2art."""
    header = text2art("idontexist-rescue", font="tarty4")
    print(colored(header, "cyan"))
    print(colored("Version 1.0 // Coded by Grahf // github.com/grahfmusic\n", "green"))


def check_sudo(verbose):
    """Check if the script is run as root, if not re-execute with sudo."""
    if os.geteuid() != 0:
        print(colored(":: Requires sudo. Re-running with sudo...", "yellow"))
        if verbose:
            print(
                colored(f":: Sudo Command: sudo python3 {' '.join(sys.argv)}", "cyan")
            )
        try:
            os.execvp("sudo", ["sudo", "python3"] + sys.argv)
        except Exception as e:
            print(colored(f":: Sudo Execution Failed: {e}", "red"))
        sys.exit(1)


def run_command_with_progress(command, verbose):
    """Run a shell command and handle real-time output."""
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    total_bytes = 0
    term_width = shutil.get_terminal_size().columns
    progress_bar_length = 20
    start_time = time.time()

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            # Remove the "to " or "from " reminder text from the output
            output = output.replace("to ", "").replace("from ", "")
            total_bytes += len(output)

            # Calculate progress
            progress = total_bytes
            total = None  # Use None if total size is unknown
            percent = progress / total if total else 0
            elapsed = time.time() - start_time

            # Build the progress bar
            filled_length = int(progress_bar_length * percent)
            progress_bar = "█" * filled_length + "-" * (
                progress_bar_length - filled_length
            )

            # Create a color gradient for the text
            text_color = Fore.BLUE + Style.BRIGHT
            text_color_end = Fore.WHITE + Style.BRIGHT
            text_gradient = [
                text_color
                + chr(
                    int(
                        i
                        * (ord(text_color_end[-1]) - ord(text_color[-1]))
                        / progress_bar_length
                    )
                    + ord(text_color[-1])
                )
                + Style.RESET_ALL
                for i in range(filled_length)
            ]
            text_gradient += [
                Fore.WHITE + Style.BRIGHT + "-" + Style.RESET_ALL
                for _ in range(progress_bar_length - filled_length)
            ]

            # Add the color gradient to the progress bar
            progress_bar = "".join(text_gradient)

            # Add different colors for the '::' separators
            separator_colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN]
            separator_color_index = int(percent * len(separator_colors))
            separator = separator_colors[separator_color_index] + "::" + Style.RESET_ALL

            progress_bar = f"{separator} [{progress_bar}] {progress}/{total if total else '?'} [{elapsed:.2f}s]"

            # Print the progress bar on the same line
            print(f"\r{progress_bar}", end="", flush=True)

            if verbose:
                print(output.strip(), end="\r", flush=True)
            else:
                print(end="\r", flush=True)

            process.stdout.close()
            process.stderr.close()
            print()  # Print a newline after the progress bar
            return process.returncode


def backup_directory(src, dest, verbose):
    """Back up a directory using shutil.copy2()."""
    print(colored(f":: Backing up {src} to {dest}", "green"))

    total_size = sum(f.stat().st_size for f in Path(src).rglob("*"))
    copied_size = 0

    with tqdm(
        total=total_size,
        desc=colored(f":: Copying {src}", "magenta"),
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for root, dirs, files in os.walk(src):
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest, os.path.relpath(src_file, src))
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                copied_size += os.path.getsize(src_file)
                pbar.update(os.path.getsize(src_file))

    print(colored(f":: Backed up {src} to {dest}", "green"))

    if verbose:
        print()  # Print an extra newline for readability in verbose mode

    return 0


def create_backup_directory(base_dir, app_name, verbose):
    """Create a timestamped backup directory."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(base_dir, f"{app_name}_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    if verbose:
        print(colored(f":: Created dir {backup_dir}", "yellow"))
    return backup_dir


def tar_directory(src_dir, verbose):
    """Compress a directory to tar.xz."""
    tar_file = f"{src_dir}.tar.xz"
    print(colored(f":: Compressing {src_dir}", "green"))
    with tarfile.open(tar_file, "w:xz") as tar:
        tar.add(src_dir, arcname=os.path.basename(src_dir))
    shutil.rmtree(src_dir)
    if verbose:
        print(colored(f":: Removed {src_dir}", "green"))
    return tar_file


def restore_backup(backup_dir, app_name, verbose):
    """Restore a backup directory or tar.xz file."""
    print(colored(f":: Restoring {app_name}", "green"))
    if backup_dir.endswith(".tar.xz"):
        with tarfile.open(backup_dir, "r:xz") as tar:
            tar.extractall(path=f"/var/lib/{app_name}")
        print(colored(f":: Extracted {backup_dir} to /var/lib/{app_name}", "green"))
    else:
        command = [
            "rsync",
            "-a",
            "--info=progress2",
            backup_dir,
            f"/var/lib/{app_name}",
        ]
        returncode = run_command_with_progress(command, verbose)
        if returncode != 0:
            print(colored(f":: Restore Error: {backup_dir}", "red"))
        else:
            print(
                colored(
                    f":: Restored from {backup_dir} to /var/lib/{app_name}", "green"
                )
            )


def backup_apps(apps, base_backup_dir, tar_option, verbose):
    """Backup specified applications."""
    for app in apps:
        paths = backup_paths.get(app)
        if paths:
            backup_dir = create_backup_directory(base_backup_dir, app, verbose)
            for path in paths:
                dest = os.path.join(backup_dir, os.path.basename(path))
                result = backup_directory(path, dest, verbose)
                if result != 0:
                    print(colored(f":: Error backing up {path}", "red"))

            if tar_option:
                tar_file = tar_directory(backup_dir, verbose)
                print(colored(f":: Compressed backup to {tar_file}", "green"))


def main():
    print_header()
    parser = argparse.ArgumentParser(
        description="Backup and Restore Utility for Linux Applications"
    )
    parser.add_argument(
        "--backup-dir",
        type=str,
        default=os.path.join(cwd, "idontexist-backups"),
        help="Specify the backup directory",
    )
    parser.add_argument(
        "--tar",
        action="store_true",
        help="Compress backup directories to tar.xz after rsync",
    )
    parser.add_argument(
        "--restore",
        type=str,
        help="Path to the backup directory or tar.xz file to restore from",
    )
    parser.add_argument(
        "--app",
        type=str,
        help="Application to backup or restore. Use 'all' to backup all applications",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    check_sudo(args.verbose)

    base_backup_dir = args.backup_dir
    os.makedirs(base_backup_dir, exist_ok=True)

    if args.restore and args.app:
        restore_backup(args.restore, args.app, args.verbose)
        print(colored(f":: Restored {args.app} from {args.restore}", "green"))
    elif args.app:
        apps_to_backup = backup_paths.keys() if args.app == "all" else [args.app]
        backup_apps(apps_to_backup, base_backup_dir, args.tar, args.verbose)
    else:
        print(
            colored(
                ":: Please specify an application to backup or restore using --app",
                "red",
            )
        )


if __name__ == "__main__":
    main()
