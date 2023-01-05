from Filter_Blocks.Main_Filter_block import Filter_main_blocks

class Interface_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()

    def interface_filter(self, core_interface, core_list):

        data_type = 'interface'
        find_interface = list(filter(lambda linea: core_interface in linea, core_list))
        block_list = self.main_filter.block(core_list, find_interface, data_type, '!', True, False)
        return block_list