from Filter_Blocks.Main_Filter_block import Filter_main_blocks
from Clean_Blocks.Get_Residential_Data import Get_residential_data
import re

class Filter_residential:

    def __init__(self, residential_parameters):

        self.residential_parameters = residential_parameters
        self.main_filter = Filter_main_blocks()
        self.clean_data = Get_residential_data()
        self.gid_routes = []
        self.iptv_unicast_routes = []
        
    def filter_data(self, ce_cfg, ce_int, version, peers_obj):

        data_type = 'residential'

        """FILTER GID1 AND IPTV UNICAST STATIC ROUTE, DEPEND OF DE CE VERSION"""
        if version == 1:
            routes =  list(filter(lambda x: 'ip route ' in x, ce_cfg))
            self.gid_routes = list(filter(lambda x: 'gid1' in x, routes))
            self.iptv_unicast_routes = list(filter(lambda x: 'IPTV-UNICAST' in x, routes))
        
        if version == 2:
            routes = self.main_filter.block(ce_cfg, ['router static'], data_type, '!', True, False)
            
            if list(filter(lambda x: ' vrf gid1' in x, routes)) != []:
                self.gid_routes = self.main_filter.block(routes, [' vrf gid1'], data_type, ' !', True, False)
            else:
                self.gid_routes = []

            if list(filter(lambda x: ' vrf IPTV-UNICAST' in x, routes)) != []:
                self.iptv_unicast_routes = self.main_filter.block(routes, [' vrf IPTV-UNICAST'], data_type, ' !', True, False)
            else:
                self.iptv_unicast_routes = []

        inter = list(filter(lambda x: ce_int in x, ce_cfg))
        filter_inter = [x for x in inter if re.findall(f'^interface', x)]
        for x in range(len(filter_inter)):
            block = self.main_filter.block(ce_cfg, [filter_inter[x]], data_type, '!', True, False)
            self.clean_data.get_data(self.residential_parameters, block, ce_cfg, self.gid_routes, self.iptv_unicast_routes, version, peers_obj)


