import re
from tkinter import messagebox

def filter_block(list, first_line, data_type, break_point):

    block = []
    #print(first_line)
    if first_line != []:
       
        first_index = int(list.index(first_line[0]))
        for x in range(first_index, len(list)):
            block.append(list[x])
            if re.findall("!", list[x]) and list[x] == break_point:
                break
    else:
        messagebox.showinfo("Warning", "The legacy interface was not found")
        exit()

    return block
