import os
import shutil
import argparse
from datetime import datetime

# ---------------------------
# 1. category keywords
# ---------------------------
CATEGORY_KEYWORDS = {
    "Math": ("math", "mathematics", "calculus", "calc", "algebra", "geometry"),
     "English": ("english", "comp", "composition", "eng", "lit", "literature",),
    "Science": ("science", "biology", "chemistry", "physics"),
    "History": ("history", "hist", "government", "civics", "gov", "social studies"),
    "Language": ("spanish", "french", "german", "language", "lang"),
    "Art": ("art", "drawing", "painting", "sketch"),
    "Documents": ("doc", "docx", "pdf", "txt"),
    "Images": ("jpg", "jpeg", "gif", "png",),
}

MIN_FILES_TO_KEEP_CATEGORY = 3  # categories with less files than 3 in them will be merged into a Misc 

# -----------------------------
# 2. Lists the files in the directory
# -----------------------------
def get_directory_files(path):
    try:
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    except Exception as e:
        print(f"[ERROR] {e}")
        return []

# -----------------------------
# 3. Categories based on keywords
# -----------------------------
def determine_categories(file_name):
    name_lower = file_name.lower()
    # Return the first matching category to avoid attempting
    # to move the same file multiple times into different folders.
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                return [category]

    return ["Other"]

# -----------------
# 4. Create folder
# -----------------
def create_folder(path, folder_name, dry_run=False):
    folder_path = os.path.join(path, folder_name)
    try:
        if os.path.exists(folder_path):
            return folder_path

        if dry_run:
            print(f"[DRY-RUN] Would create folder: {folder_path}")
            return folder_path

        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
        return folder_path
    except Exception as e:
        print(f"[ERROR] folder not able to be created {folder_name}: {e}")
        return None

# -----------------
# 5. Move file
# -----------------
def move_file(file_path, destination_path, dry_run=False):
    try:
        if dry_run:
            print(f"[DRY-RUN] Would move: {os.path.basename(file_path)} → {destination_path}")
            return

        shutil.move(file_path, destination_path)
        print(f"Moved: {os.path.basename(file_path)} → {destination_path}")
    except Exception as e:
        print(f"[ERROR] Could not move file: {file_path} → {destination_path}: {e}")

# -----------------
# 6. Organize files by name & subfolders by month created
# -----------------
def organize_files(path, dry_run=False):
    print("\n---FILE ORGANIZER ---")
    files = get_directory_files(path)
    if not files:
        print("[ERROR] No files to organize.")
        return

    category_file_count = {}

    for file_path in files:
        file_name = os.path.basename(file_path)
        categories = determine_categories(file_name)  # returns single-item list

        for category in categories:
            # First: category folder
            category_folder = create_folder(path, category, dry_run=dry_run)

            # Next: Month subfolder
            try:
                timestamp = os.path.getmtime(file_path)
                month_folder_name = datetime.fromtimestamp(timestamp).strftime("%Y-%m")
            except Exception:
                month_folder_name = "UnknownMonth"

            month_folder = create_folder(category_folder, month_folder_name, dry_run=dry_run)

            # Next: Move file
            if month_folder:
                move_file(file_path, month_folder, dry_run=dry_run)

            # Count files per category
            category_file_count[category] = category_file_count.get(category, 0) + 1

    # Next: Less than MIN files in category are moved to Misc folder
    for category, count in category_file_count.items():
        if count < MIN_FILES_TO_KEEP_CATEGORY and category != "Misc":
            category_folder = os.path.join(path, category)
            misc_folder = create_folder(path, "Misc", dry_run=dry_run)
            try:
                for root, _, files in os.walk(category_folder):
                    for f in files:
                        file_path = os.path.join(root, f)
                        move_file(file_path, misc_folder, dry_run=dry_run)
                # Remove folder
                if dry_run:
                    print(f"[DRY-RUN] Would remove folder: {category_folder}")
                else:
                    shutil.rmtree(category_folder)
                    print(f"Category '{category}' moved into Misc")
            except Exception as e:
                print(f"[ERROR] Could not merge {category} into Misc: {e}")

# =============
# MAIN PROGRAM
# =============
def _parse_args():
    parser = argparse.ArgumentParser(description="Organize files into category/month folders")
    parser.add_argument("folder", nargs="?", help="Folder path to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without making changes")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    folder_to_sort = args.folder or input("folder path to organize: ")
    if os.path.exists(folder_to_sort):
        organize_files(folder_to_sort, dry_run=args.dry_run)
    else:
        print("[ERROR] This folder does not exist.")