import subprocess
import os

# U stand for unmerged
U_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, shell=True)
# M stands for modified
M_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=M"], capture_output=True, shell=True)
# Files that newly added in the commit, and thus act like normally added files.
simply_added_result = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=A"], capture_output=True,
                                     shell=True)

U_result_set = set(U_result.stdout.split(b'\n'))
M_result_set = set(M_result.stdout.split(b'\n'))
simply_added_result_set = set(simply_added_result.stdout.split(b'\n'))

U_result_set = U_result_set.difference(M_result_set)
all_files = simply_added_result_set.union(U_result_set)

all_files = [os.path.normpath(file_path.decode("utf-8-sig")) for file_path in all_files if file_path]

chunk_size = 100  # adjust this as needed
for i in range(0, len(all_files), chunk_size):
    subprocess.run(["git", "rm", "-f"] + all_files[i:i + chunk_size])