from Filter_Blocks.Main_Filter_block import Filter_main_blocks
import re

class Policy_filter_block:

    def __init__(self):

        self.main_filter = Filter_main_blocks()

    def policy_filter(self, parameters, patterns, core_list, key_one, key_two):

        data_type = 'traffic_policy'
        policy = parameters[key_one][key_two]

        first_line = list(filter(lambda x: f'policy-map {policy}' in x, core_list))
        if first_line != []:
            block_list = self.main_filter.block(core_list, first_line, data_type, '!', True, False)
            block_list.remove(block_list[0])
            block_list.remove(block_list[len(block_list) - 1])
            return block_list
        else:
            return []

            


