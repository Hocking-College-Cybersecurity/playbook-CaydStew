"""
File Organizer Script
---------------------
Organizes files into category folders and month subfolders, logs operations,
and merges small categories into a Misc folder.

Features:
    • Categorization by filename keywords
    • Month-based subfolder organization
    • File I/O: JSON log load + save
    • Dry-run mode for previewing actions
    • Robust error handling and directory cleanup
    • Professional commenting and structure
"""

import os
import shutil
import json
import argparse
from datetime import datetime

# -------------------------------------------------------------------
# 1. CATEGORY DEFINITIONS
# -------------------------------------------------------------------

CATEGORY_KEYWORDS = {
    "Math": ("math", "mathematics", "calculus", "calc", "algebra", "geometry"),
    "English": ("english", "comp", "composition", "eng", "lit", "literature"),
    "Science": ("science", "biology", "chemistry", "physics"),
    "History": ("history", "hist", "government", "civics", "gov", "social studies"),
    "Language": ("spanish", "french", "german", "language", "lang"),
    "Art": ("art", "drawing", "painting", "sketch"),
    "Documents": ("doc", "docx", "pdf", "txt"),
    "Images": ("jpg", "jpeg", "gif", "png"),
}

# Categories with fewer than this many files get merged into "Misc"
MIN_FILES_TO_KEEP_CATEGORY = 3

# Default log filename
LOG_FILE = "organizer_log.json"


# -------------------------------------------------------------------
# 2. FILE I/O (SAVE + LOAD LOG)
# -------------------------------------------------------------------
def load_log(path):
    """Load previous log file if present."""
    log_path = os.path.join(path, LOG_FILE)
    if not os.path.exists(log_path):
        return []

    try:
        with open(log_path, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_log(path, log):
    """Save the organizer log to a JSON file."""
    log_path = os.path.join(path, LOG_FILE)
    try:
        with open(log_path, "w") as f:
            json.dump(log, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Unable to save log: {e}")


# -------------------------------------------------------------------
# 3. FILE RETRIEVAL
# -------------------------------------------------------------------
def get_directory_files(path):
    """Return a list of file paths in the directory (non-recursive)."""
    try:
        return [
            os.path.join(path, f)
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f))
        ]
    except Exception as e:
        print(f"[ERROR] {e}")
        return []


# -------------------------------------------------------------------
# 4. CATEGORY DETECTION
# -------------------------------------------------------------------
def determine_category(file_name):
    """Return the first matching category based on keywords."""
    name = file_name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in name for kw in keywords):
            return category
    return "Other"


# -------------------------------------------------------------------
# 5. DIRECTORY CREATION
# -------------------------------------------------------------------
def create_folder(path, folder_name, dry_run=False):
    """Create folder if it does not exist."""
    full_path = os.path.join(path, folder_name)
    if os.path.exists(full_path):
        return full_path

    if dry_run:
        print(f"[DRY-RUN] Would create folder: {full_path}")
        return full_path

    try:
        os.makedirs(full_path)
        print(f"Created folder: {full_path}")
        return full_path
    except Exception as e:
        print(f"[ERROR] Unable to create folder '{folder_name}': {e}")
        return None


# -------------------------------------------------------------------
# 6. MOVE FILES
# -------------------------------------------------------------------
def move_file(file_path, destination_path, dry_run, log):
    """Move file safely with logging."""
    file_name = os.path.basename(file_path)

    if dry_run:
        print(f"[DRY-RUN] Would move: {file_name} → {destination_path}")
        return

    try:
        shutil.move(file_path, destination_path)
        log.append({"action": "move", "file": file_name, "to": destination_path})
        print(f"Moved: {file_name} → {destination_path}")
    except Exception as e:
        print(f"[ERROR] Could not move {file_name}: {e}")


# -------------------------------------------------------------------
# 7. ORGANIZER CORE LOGIC
# -------------------------------------------------------------------
def organize_files(path, dry_run=False):
    print("\n--- FILE ORGANIZER ---")

    files = get_directory_files(path)
    if not files:
        print("[ERROR] No files to organize.")
        return

    log = load_log(path)
    category_counts = {}

    # --- MAIN FILE ORGANIZATION LOOP ---
    for file_path in files:
        file_name = os.path.basename(file_path)
        category = determine_category(file_name)

        category_folder = create_folder(path, category, dry_run)

        # Determine month folder
        try:
            timestamp = os.path.getmtime(file_path)
            month_folder_name = datetime.fromtimestamp(timestamp).strftime("%Y-%m")
        except Exception:
            month_folder_name = "UnknownMonth"

        month_folder = create_folder(category_folder, month_folder_name, dry_run)

        # Move file into month folder
        move_file(file_path, month_folder, dry_run, log)

        category_counts[category] = category_counts.get(category, 0) + 1

    # --- MERGE SMALL CATEGORIES ---
    misc_folder = create_folder(path, "Misc", dry_run)
    for category, count in category_counts.items():
        if count < MIN_FILES_TO_KEEP_CATEGORY and category != "Misc":
            category_folder = os.path.join(path, category)
            if not os.path.exists(category_folder):
                continue

            print(f"Merging small category '{category}' → Misc")

            # Move all files from category folder
            for root, _, files in os.walk(category_folder):
                for f in files:
                    file_path = os.path.join(root, f)
                    move_file(file_path, misc_folder, dry_run, log)

            # Remove empty category folder
            if dry_run:
                print(f"[DRY-RUN] Would delete: {category_folder}")
            else:
                shutil.rmtree(category_folder, ignore_errors=True)
                log.append({"action": "delete_folder", "folder": category_folder})

    # Save log file
    save_log(path, log)


# -------------------------------------------------------------------
# 8. MAIN ENTRY
# -------------------------------------------------------------------
def _parse_args():
    parser = argparse.ArgumentParser(description="Organize files into category/month folders.")
    parser.add_argument("folder", nargs="?", help="Folder path to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without changes")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    folder = args.folder or input("Folder path to organize: ")

    if os.path.exists(folder):
        organize_files(folder, dry_run=args.dry_run)
    else:
        print("[ERROR] Folder does not exist.")
