import re

class Service_template:

    def __init__(self, parameters):

        self.parameters = parameters
        self.vpn = parameters['INTER']['VPN'] if parameters['INTER']['VPN'] != "" else 'INFOINTERNET'

    def policy_service(self, policy_template):
                                                    
        for x in range(len(self.parameters['POLICY_IN'])):
            policy_template[6] = policy_template[6].replace('number_one', self.parameters['POLICY_IN'][x]) if x == 0 else policy_template[6]
            policy_template[6] = policy_template[6].replace('number_two', self.parameters['POLICY_IN'][x]) if x == 1 else policy_template[6]
            policy_template[6] = policy_template[6].replace('number_tree', self.parameters['POLICY_IN'][x]) if x == 2 else policy_template[6]

        policy_template[6] = policy_template[6].replace('car cir number_one', "")
        policy_template[6] = policy_template[6].replace('cbs number_two', "")
        policy_template[6] = policy_template[6].replace('pbs number_tree green pass red discard', "")

        policy_template = [x.replace('ENLACE_XX', self.parameters['INTER']['POLICY_IN']) for x in policy_template]

        return policy_template
    
    def prefix_service(self):

        prefix = self.parameters['IP_PREFIX']
        prefix_to_huawei = []

        if not re.findall('ip ip-prefix', "".join(prefix)):
            for x in prefix:
                x = x.replace('ip prefix-list ', 'ip ip-prefix ').replace(' seq ', ' index ').replace(' le ', ' less-equal ').replace('/', ' ')
                prefix_to_huawei.append(x)
        
            prefix_to_huawei.append('#\n')
        
        else: prefix_to_huawei = prefix
        
        return prefix_to_huawei

    def map_service(self, template_map, num, in_out):
        
        if in_out == 'in':
            main_key = 'ROUTE_MAP_IN'
            bgp_key = 'route-policy_in'
            
        if in_out == 'out':
            main_key = 'ROUTE_MAP_OUT'
            bgp_key = 'route-policy_out'

        template = template_map.copy()
        map = self.parameters[main_key]

        template[0] = template[0].replace('NAME_POLICY', self.parameters['BGP']['ATTRIBUTES'][bgp_key][1])
        template[0] = template[0].replace('NAME_RULE', 'permit') if map['rule'][num][0] == True and map['rule'][num][1] != "" else template[0]
        template[0] = template[0].replace('NAME_RULE', 'deny') if map['rule'][num][0] == False and map['rule'][num][1] != "" else template[0]
        template[0] = template[0].replace('NUMBER_RULE', map['rule'][num][1]) if map['rule'][num][1] != '' else template[0]
        
        if map['set local-preference'][num][0] ==True:
            template[1] = template[1].replace('TO_REPLACE', map['set local-preference'][num][1])
        
        if map['match ip address prefix-list'][num][0] == True:
            template[2] = template[2].replace('TO_REPLACE', map['match ip address prefix-list'][num][1])

        if map['match interface'][num][0] == True:
            pass #SET ALARM
            
        if map['set as-path prepend'][num][0] == True:
            template[5] = template[5].replace('TO_REPLACE', map['set as-path prepend'][num][1])

        if map['set extcommunity'][num][0] == True:
            rt = map['set extcommunity'][num][1]
            for i in range(len(map['set extcommunity'][num][1])):
                template[7] = template[7].replace('TO_REPLACE', '')
                template[7] = template[7] + f' rt {rt[i]}'
                if i == len(rt)-1:
                    template[7] = template[7] + '\n'
            
        if map['match tag'][num][0] == True:
            template[8] = template[8].replace('TO_REPLACE', map['match tag'][num][1])
        
        if map['match ipv6 address prefix-list'][num][0] == True:
            pass  #SET ALARM
            
        template = [x for x in template if not re.findall('TO_REPLACE', x)]

        return template
            
    def vpn_service(self, vpn_template):
        
        vpn_template[0] = vpn_template[0].replace('VPN_NAME', self.vpn)
        vpn_template[1] = vpn_template[1].replace('VPN_DESCRIPTION', self.parameters['VPN']['DESCRIP'])
        vpn_template[3] = vpn_template[3].replace('ROUTE_DISTINGUISHER', self.parameters['VPN']['RD'])

        def target(vpn_target, to_replace, to_insert, num):
            for x in range(len(vpn_target)):
                vpn_template[num] = vpn_template[num].replace(to_replace, vpn_target[x])
                if x < len(vpn_target):
                    vpn_template.insert(num+1, to_insert)
                    num += 1

        target(self.parameters['VPN']['RTE'], 'RTE_NUMBER', '  vpn-target RTE_NUMBER export-extcommunity\n', 4)
        num = vpn_template.index('  vpn-target RTI_NUMBER import-extcommunity\n')
        target(self.parameters['VPN']['RTI'], 'RTI_NUMBER', '  vpn-target RTI_NUMBER import-extcommunity\n', num)
        vpn_template.remove('  vpn-target RTE_NUMBER export-extcommunity\n')
        vpn_template.remove('  vpn-target RTI_NUMBER import-extcommunity\n')

        return vpn_template

    def rip_service(self, rip_template):
         
        def peer(peer_type, to_replace, to_insert, num):

            for x in range(len(peer_type)):
                rip_template[num] = rip_template[num].replace(to_replace, peer_type[x])
                if x < len(peer_type):
                    rip_template.insert(num+1, to_insert)
                    num += 1

        if self.parameters['RIP']['network'] != []:
            peer(self.parameters['RIP']['network'], 'PEER_IP', ' network PEER_IP\n', 2)
        if self.parameters['RIP']['neighbor'] != []:
            peer(self.parameters['RIP']['neighbor'], 'PEER_IP', ' peer PEER_IP\n', rip_template.index(' peer PEER_IP\n'))

        ref = self.parameters['INTER']['REF']
        rip_template[0] = rip_template[0].replace('RIP_NUMBER', ref) if ref != "" else rip_template[0].replace('RIP_NUMBER', 'XXXXX')
        rip_template[0] = rip_template[0].replace('VPN_NAME', self.vpn)

        rip_template.remove(' network PEER_IP\n')
        rip_template.remove(' peer PEER_IP\n')
        rip_template = [x for x in rip_template if not re.findall('PEER_IP', x)]

        return rip_template
                

    def bgp_service(self, template):

        bgp = self.parameters['BGP']['ATTRIBUTES']
        peer = self.parameters['BGP']['PEER']

        template[1] = template[1].replace('VPN_NAME', self.vpn)
        template[4] = template[4].replace('TO_REPLACE', bgp['import-route rip'][1]) if bgp['import-route rip'][0] == True else template[4]
        template[5] = template[5].replace('TO_REPLACE', bgp['maximum load'][1]) if bgp['maximum load'][0] == True else template[5]
        template[6] = template[6].replace('TO_REPLACE', bgp['as-number'][1]) if bgp['as-number'][0] == True else template[6]
        template[7] = template[7].replace('TO_REPLACE', bgp['description'][1]) if bgp['description'][0] == True else template[7]
        template[12] = template[12].replace('TO_REPLACE', bgp['route-limit'][1]) if bgp['route-limit'][0] == True else template[12]
        template[14] = template[14].replace('TO_REPLACE', bgp['password cipher'][1]) if bgp['password cipher'][0] == True else template[14]
        template[15] = template[15].replace('TO_REPLACE', bgp['ebgp-max-hop'][1]) if bgp['ebgp-max-hop'][0] == True else template[15]
        template[16] = template[16].replace('TO_REPLACE', bgp['allow-as-loop'][1]) if bgp['allow-as-loop'][0] == True else template[16]
        template[17] = template[17].replace('TO_REPLACE', bgp['route-update'][1]) if bgp['route-update'][0] == True else template[17]
        template[19] = template[19].replace('TO_REPLACE', bgp['route-policy_in'][1]) if bgp['route-policy_in'][0] == True else template[19]
        template[20] = template[20].replace('TO_REPLACE', bgp['route-policy_out'][1]) if bgp['route-policy_out'][0] == True else template[20]

        template.remove(' import-route static\n') if bgp['import-route static'][0] == False else template[3]
        template.remove(' peer IP_PEER advertise-community\n') if bgp['advertise-community'][0] == False else template[8]
        template.remove(' peer IP_PEER keep-all-routes\n') if bgp['keep-all-routes'][0] == False else template[9]
        template.remove(' peer IP_PEER substitute-as\n') if bgp['substitute-as'][0] == False else template[10]
        template.remove(' peer IP_PEER default-route-advertise\n') if bgp['default-route-advertise'][0] == False else template[13]
        template.remove(' peer IP_PEER reflect-client\n') if bgp['reflect-client'][0] == False else template[18]

        template = [x.replace('IP_PEER', peer) for x in template] if peer != "" else template
        template = [x for x in template if not re.findall('IP_PEER', x )]
        template = [x for x in template if not re.findall('TO_REPLACE', x)]
                
        return template

    def flow_service(self, template): 

        flow = self.parameters['FLOW_QUEUE']
        
        template[0] = template[0].replace('SERVICE_POLICY', self.parameters['POLICY_OUT']['service-policy'])
        template[10] = template[10].replace('QOS_PROFILE', self.parameters['INTER']['POLICY_OUT'])
        template[11] = template[11].replace('SERVICE_POLICY', self.parameters['POLICY_OUT']['service-policy'])
        template[11] = template[11].replace('SHAPE_AVERAGE', self.parameters['POLICY_OUT']['shape average'])
    
        template[1] = template[1].replace('PERCENT_NUMBER', flow[' class MM'][1]) if flow[' class MM'][0] == True else template[1]
        template[2] = template[2].replace('PERCENT_NUMBER', flow[' class PLATA'][1]) if flow[' class PLATA'][0] == True else template[2]
        template[3] = template[3].replace('PERCENT_NUMBER', flow[' class ORO'][1]) if flow[' class ORO'][0] == True else template[3]
        template[4] = template[4].replace('PERCENT_NUMBER', flow[' class PLATINO'][1]) if flow[' class PLATINO'][0] == True else template[4]
        template[5] = template[5].replace('PERCENT_NUMBER', flow[' class VIDEO'][1]) if flow[' class VIDEO'][0] == True else template[5]
        template[6] = template[6].replace('PERCENT_NUMBER', flow[' class BRONCE'][1]) if flow[' class BRONCE'][0] == True else template[6]
        
        template = [x for x in template if not re.findall('PERCENT_NUMBER', x)]

        return template
    
    def interface_service(self, template, cabling_type):

        inter = self.parameters['INTER']

        template[0] = template[0].replace('X/X/X', self.parameters['NEW_INTERFACE'])
        template[5] = template[5].replace('VPN_NAME', self.vpn)

        template[6] = template[6].replace('NAME_SERVICE', inter['DESCRIP']) if inter['DESCRIP'] != "" else template[6]
        template[7] = template[7].replace('NAME_SERVICE', inter['IP']+' '+inter['MASK']) if inter['IP'] != "" else template[7]
        template[8] = template[8].replace('NAME_SERVICE', inter['IP_SEC']+' '+inter['MASK_SEC']) if inter['IP_SEC'] != "" else template[8] 
        template[9] = template[9].replace('NAME_SERVICE', inter['POLICY_IN']) if inter['POLICY_IN'] != "" else template[9]

        if inter['POLICY_OUT'] != "" and inter['POLICY_OUT'] == inter['POLICY_IN']:
            template[10] = template[10].replace('NAME_SERVICE', inter['POLICY_OUT'])
        if inter['POLICY_OUT'] != "" and inter['POLICY_OUT'] != inter['POLICY_IN']:
            template[11] = template[11].replace('NAME_SERVICE', inter['POLICY_OUT'])

        if inter['VLAN_ONE'] != "" and inter['VLAN_TWO'] != "":
            if cabling_type == 'fiber':
                template[0] = template[0].replace('VLANC', inter['VLAN_ONE'] + inter['VLAN_TWO'])
                template[4] = template[4].replace('VLANUNO', inter['VLAN_ONE'])
                template[4] = template[4].replace('VLANDOS', inter['VLAN_TWO'])
                template.remove(' Vlan-type dot1q VLANUNO\n')

            if cabling_type == 'electric':
                template[0] = template[0].replace('VLANC', inter['VLAN_TWO'])
                template[2] = template[2].replace('VLANUNO', inter['VLAN_TWO'])
                template.remove(' encapsulation qinq-termination\n')
                template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
                template.remove(' arp broadcast enable\n')

        if inter['VLAN_ONE'] != "" and inter['VLAN_TWO'] == "":
            if cabling_type == 'fiber':
                template[0] = template[0].replace('VLANC', inter['VLAN_ONE'])
                template[2] = template[2].replace('VLANUNO', inter['VLAN_ONE'])
                template.remove(' encapsulation qinq-termination\n')
                template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
                template.remove(' arp broadcast enable\n')

            if cabling_type == 'electric':
                template[0] = template[0].replace('.VLANC', "")
                template.remove(' Vlan-type dot1q VLANUNO\n')
                template.remove(' encapsulation qinq-termination\n')
                template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
                template.remove(' arp broadcast enable\n')

        if inter['VLAN_ONE'] == "" and inter['VLAN_TWO'] == "":
            template[0] = template[0].replace('.VLANC', '')
            template.remove(' Vlan-type dot1q VLANUNO\n')
            template.remove(' encapsulation qinq-termination\n')
            template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
            template.remove(' arp broadcast enable\n')

        template.remove(' shutdown\n') if inter['STATUS'] == "" else template
        if not re.findall('/', self.parameters['NEW_INTERFACE']):
            template[0] = template[0].replace('GigabitEthernet', 'Eth-Trunk')

        template = [x for x in template if not re.findall('NAME_SERVICE', x)]

        return template

    def routes_service(self, routes_template):

        routes_service = []
        for x in range(len(self.parameters['ROUTES'])):
            route = routes_template[0].replace('VPN_NAME', self.vpn)
            route = route.replace('IPFINAL_MASK_IPPEER', self.parameters['ROUTES'][x])
            if self.parameters['INTER']['REF'] != "":
                route = route.replace('REF_NAME', self.parameters['INTER']['REF'])
            routes_service.append(route)

        return routes_service



