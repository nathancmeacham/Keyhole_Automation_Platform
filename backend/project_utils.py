# project_utils.py
import os

def count_files(directory='.'):
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

def list_files(directory='.'):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), directory))
    return file_list