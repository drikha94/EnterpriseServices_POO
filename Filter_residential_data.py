from Filter_Blocks.Main_Filter_block import Filter_main_blocks
from Get_Residential_Data import Get_residential_data
import re

class Filter_residential:

    def __init__(self, parameters):

        self.parameters = parameters
        self.main_filter = Filter_main_blocks()
        self.clean_data = Get_residential_data()

    def filter_data(self, ce_cfg, ce_int):

        data_type = 'residential'
        inter = list(filter(lambda x: ce_int in x, ce_cfg))
        #for x in range(len(inter)):
            #if re.findall(r'[.]\d+', inter[x]):
        block = self.main_filter.block(ce_cfg, [inter[4]], data_type, '!', True, False)
        self.clean_data.get_data(self.parameters, block)


