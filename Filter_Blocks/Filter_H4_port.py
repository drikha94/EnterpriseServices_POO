import re
from Filter_Blocks.Main_Filter_block import Filter_main_blocks

class Filter_h4_port:

    def __init__(self, h4_cfg, interface):

        self.h4_cfg = h4_cfg
        self.interface = list(filter(lambda linea: f'{interface} current state' in linea, self.h4_cfg))
        self.last_line = 'Last 30 seconds output utility rate'
        self.main_filter = Filter_main_blocks()

    def interfaces_filter(self):

        data_type = 'h4_port'
        block_list = []

        if self.interface != []:
            block_list = self.main_filter.block(self.h4_cfg, self.interface, data_type, self.last_line, True, False)

        return block_list









