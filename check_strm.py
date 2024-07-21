#!/usr/local/bin/python3

import os

def check_strm_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".strm"):
                return True
    return False

def print_directories_without_strm(directory):
    for root, dirs, files in os.walk(directory):
        if not root.endswith(".actors"):
            if not check_strm_files(root):
                print(root.replace("/media/",""))

directory_to_check = "/media"

print_directories_without_strm(directory_to_check)
