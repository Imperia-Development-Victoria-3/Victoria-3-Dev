# Python3 code to Check for
# balanced parentheses in an expression
import os, glob
import codecs
open_list = ["[","{","("]
close_list = ["]","}",")"]
yourpath = os.path.dirname(__file__)

# Check if file is utf-8 with bom
def is_utf8_with_bom(file_path):
    with open(file_path, 'rb') as file:
        # Read the first 4 bytes to check for the BOM
        data = file.read(4)
        return data[:3] == codecs.BOM_UTF8

def process_file(file_path):
    if not is_utf8_with_bom(file_path):
        print(f"NOT UTF-8 w/BOM: {file_path}")
        return
    text = ""
    with open(file_path, 'r', encoding='utf-8-sig') as newfile:
        for line in newfile:
            text += line
    print(check(text),"-",file_path)
        
# Function to check parentheses
def check(myStr):
    stack = []
    for i in myStr:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return "Unbalanced"
    if len(stack) == 0:
        return "Balanced"
    else:
        return "Unbalanced"

# Go on a walk
for root, dirs, files in os.walk(yourpath):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            process_file(file_path)