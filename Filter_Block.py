import re
from tkinter import messagebox

def filter_block(core_list, first_line, data_type):

    block = []
    print(first_line)
    if first_line != []:
       
        first_index = int(core_list.index(first_line[0]))
        for x in range(first_index, len(core_list)):
            block.append(core_list[x])
            if re.findall("!", core_list[x]) and core_list[x] == "!":
                break
    else:
        messagebox.showinfo("Warning", "The legacy interface was not found")
        exit()

    return block
