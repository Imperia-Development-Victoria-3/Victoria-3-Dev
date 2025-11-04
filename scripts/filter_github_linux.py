#!/usr/bin/env python3

import subprocess
import os

# Move to the root of the Git repo
repo_root = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    capture_output=True,
    text=True,
    check=True
).stdout.strip()
os.chdir(repo_root)

# Get lists of files from git diff
U_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, check=True)
M_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=M"], capture_output=True, check=True)
simply_added_result = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
    capture_output=True,
    check=True
)

# Decode and split outputs
U_result_set = set(U_result.stdout.decode("utf-8").splitlines())
M_result_set = set(M_result.stdout.decode("utf-8").splitlines())
simply_added_result_set = set(simply_added_result.stdout.decode("utf-8").splitlines())

# Exclude modified from unmerged
U_result_set.difference_update(M_result_set)

# Combine the sets
all_files = simply_added_result_set.union(U_result_set)

# Normalize paths
all_files = [os.path.normpath(path) for path in all_files if path]

# Chunked removal with index check
chunk_size = 100
for i in range(0, len(all_files), chunk_size):
    chunk = all_files[i:i + chunk_size]

    # Only include files that exist in Git index
    valid_files = []
    for file in chunk:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            valid_files.append(file)
        else:
            print(f"Skipped (not in index): {file}")

    if valid_files:
        subprocess.run(["git", "rm", "-f"] + valid_files, check=True)

