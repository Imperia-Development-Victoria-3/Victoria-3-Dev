import subprocess

# U stand for unmerged
U_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=U"], capture_output=True, shell=True)
# D stands for deleted
D_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=D"], capture_output=True, shell=True)
# A stands for added
A_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=A"], capture_output=True, shell=True)
# M stands for modified
M_result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=M"], capture_output=True, shell=True)
# Files that newly added in the commit, and thus act like normally added files.
simply_added_result = subprocess.run(["git", "diff",  "--cached", "--name-only", "--diff-filter=A"], capture_output=True, shell=True)

U_result_set = set(U_result.stdout.split(b'\n'))
D_result_set = set(D_result.stdout.split(b'\n'))
A_result_set = set(A_result.stdout.split(b'\n'))
M_result_set = set(M_result.stdout.split(b'\n'))
simply_added_result_set = set(simply_added_result.stdout.split(b'\n'))

U_result_set = U_result_set.difference(M_result_set)

for file_path in U_result_set.union(D_result_set):
	subprocess.run(["git", "rm", file_path], shell=True)

for file_path in U_result_set.union(A_result_set).difference(D_result_set):
	subprocess.run(["git", "rm", "-f", file_path], shell=True)

for file_path in simply_added_result_set:
	subprocess.run(["git", "rm", "-f", file_path], shell=True)