import re
from tkinter import messagebox

class Filter_main_blocks:

    def block(self, list, first_line, data_type, break_point, validation, space):

        block = []

        if first_line != []: 
            
            first_index = int(list.index(first_line[0]))

            for x in range(first_index, len(list)):
                block.append(list[x])
                if validation == False and data_type != 'traffic_policy':
                    if re.findall(break_point, list[x]):
                        break

                if validation == True and data_type != 'traffic_policy':
                    if re.findall(break_point, list[x]) and list[x] == break_point:
                        break

                if data_type == 'traffic_policy':
                    if re.findall("policy-map", list[x]) and x > first_index:
                        break
                    if re.findall(break_point, list[x]) and list[x] == break_point:
                        break

            if space == True:
                block_bkp = block
                block = []
                for x in block_bkp:
                    block.append(f'{x} ')

        else:
            messagebox.showinfo("Warning", "The legacy interface was not found")
            exit()

        return block




