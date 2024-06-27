#!/usr/bin/env python3

import os
import time
import subprocess
import datetime
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

# Define backup paths (unchanged)
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
                colored(f":: Sudo Command: {' '.join(sys.argv)}", "cyan")
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
            total_bytes += len(output)

            # Calculate progress
            progress = total_bytes
            total = None  # Use None if total size is unknown
            percent = progress / total if total else 0
            elapsed = time.time() - start_time

            # Build the progress bar (unchanged)
            filled_length = int(progress_bar_length * percent)
            progress_bar = "█" * filled_length + "-" * (
                progress_bar_length - filled_length
            )

            # Add the color gradient to the progress bar (unchanged)
            progress_bar = "".join(
                [
                    Fore.BLUE + Style.BRIGHT + char + Style.RESET_ALL
                    for char in progress_bar[:filled_length]
                ]
            ) + "".join(
                [
                    Fore.WHITE + Style.BRIGHT + "-" + Style.RESET_ALL
                    for _ in range(progress_bar_length - filled_length)
                ]
            )

            # Add different colors for the '::' separators (unchanged)
            separator_colors = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN]
            separator_color_index = int(percent * len(separator_colors))
            separator = separator_colors[separator_color_index] + "::" + Style.RESET_ALL

            progress_bar = f"{separator} [{progress_bar}] {progress}/{total if total else '?'} [{elapsed:.2f}s]"

            # Print the progress bar on the same line (unchanged)
            print(f"\r{progress_bar}", end="", flush=True)

            if verbose:
                print(output.strip(), end="\r", flush=True)
            else:
                print(end="\r", flush=True)

    process.stdout.close()
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
        ncols=80,
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

def restore_backup(backup_dir, app_name, verbose):
    """Restore a backup directory."""
    print(colored(f":: Restoring {app_name}", "green"))

    # Example for directory restoration, modify as per your needs
    command = [
        "rsync",
        "-a",
        "--info=progress2",
        backup_dir,
        f"/var/lib/{app_name}",
    ]
    returncode = run_command_with_progress(command, verbose)
    if returncode != 0:
        print(colored(f":: Restore failed with exit code {returncode}", "red"))
    else:
        print(colored(f":: Restored {backup_dir} to /var/lib/{app_name}", "green"))

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Backup and restore utility for application directories."
    )
    parser.add_argument(
        "-b", "--backup", action="store_true", help="Perform a backup operation."
    )
    parser.add_argument(
        "-r", "--restore", action="store_true", help="Perform a restore operation."
    )
    parser.add_argument(
        "-a", "--app", type=str, default="all", choices=list(backup_paths.keys()) + ["all"],
        help="Specify the application to backup or restore, or 'all' for all applications."
    )
    parser.add_argument(
        "-d", "--directory", type=str, default=os.path.join(cwd, "idontexist-backups"),
        help="Specify the backup/restore directory. Default is 'idontexist-backups' in the current working directory."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    return parser.parse_args()

def main():
    print_header()
    args = parse_args()

    check_sudo(args.verbose)

    if args.backup:
        if args.app == "all":
            for app_name, paths in backup_paths.items():
                backup_dir = create_backup_directory(args.directory, app_name, args.verbose)
                for path in paths:
                    backup_directory(path, backup_dir, args.verbose)
                print(colored(f":: Backup completed for {app_name}.", "green"))
        else:
            if args.app not in backup_paths:
                print(colored(f":: Application '{args.app}' not found in backup_paths.", "red"))
                sys.exit(1)
            paths = backup_paths[args.app]
            backup_dir = create_backup_directory(args.directory, args.app, args.verbose)
            for path in paths:
                backup_directory(path, backup_dir, args.verbose)
            print(colored(f":: Backup completed for {args.app}.", "green"))

    elif args.restore:
        if args.app == "all":
            backup_files = os.listdir(args.directory)
            for backup_file in backup_files:
                restore_backup(os.path.join(args.directory, backup_file), backup_file.split("_")[0], args.verbose)
        else:
            restore_backup(args.directory, args.app, args.verbose)

    else:
        print(colored(":: No operation specified. Use -b/--backup or -r/--restore.", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main()
