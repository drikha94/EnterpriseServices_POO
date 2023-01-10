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

    def bgp_service(self, bgp_template):

        """CUALQUIER COMANDO QUE SE QUIERA AGREGAR ES NECESARIO AGREGARLO TAMBIEN EN EL 
        ARCHIVO Establish_Parameters.py EN EL MISMO ORDEN EN EL QUE SE AGREGE EN EL TEMPLATE, 
        CON SU RESPECTIVA CONFIRMACION BOOLEANA"""

        if self.parameters['BGP']['PEER'] == "":
            self.parameters['BGP']['ATTRIBUTES']['fake-as'][0] = False
            self.parameters['BGP']['ATTRIBUTES']['enable'][0] = False
        
        bgp_template = [x.replace('IP_PEER', self.parameters['BGP']['PEER']) for x in bgp_template]
        bgp_template[1] = bgp_template[1].replace('VPN_NAME', self.vpn)
        bgp_template[4] = bgp_template[4].replace('RIP_NUMBER', self.parameters['BGP']['ATTRIBUTES']['import-route rip'][1])
        bgp_template[5] = bgp_template[5].replace('BALANCING_NUMBER', self.parameters['BGP']['ATTRIBUTES']['maximum load-balancing ibgp'][1])
        bgp_template[6] = bgp_template[6].replace('AS_NUMBER', self.parameters['BGP']['ATTRIBUTES']['as-number'][1])
        bgp_template[7] = bgp_template[7].replace('BGP_DESCRIPTION', self.parameters['BGP']['ATTRIBUTES']['description'][1])
        bgp_template[12] = bgp_template[12].replace('ROUTE_LIMIT', self.parameters['BGP']['ATTRIBUTES']['route-limit'][1])
        bgp_template[14] = bgp_template[14].replace('PASSWORD_CIPHER', self.parameters['BGP']['ATTRIBUTES']['password cipher'][1])
        bgp_template[15] = bgp_template[15].replace('MAX_HOP_NUMBER', self.parameters['BGP']['ATTRIBUTES']['ebgp-max-hop'][1])
        bgp_template[16] = bgp_template[16].replace('ALLOW_IN_NUMBER', self.parameters['BGP']['ATTRIBUTES']['allow-as-loop'][1])
        bgp_template[17] = bgp_template[17].replace('ROUTE_INTERVAL_NUMBER', self.parameters['BGP']['ATTRIBUTES']['route-update-interval'][1])

        confirmation = []
        for x in self.parameters['BGP']['ATTRIBUTES'].values():
            confirmation.append(x[0])
        
        bgp_template_bkp = bgp_template
        bgp_template = []
        for x in range(len(bgp_template_bkp)):
            if confirmation[x] == True:
                bgp_template.append(bgp_template_bkp[x])
                
        return bgp_template

    def flow_service(self, flow_template): 
        
        flow_template[0] = flow_template[0].replace('SERVICE_POLICY', self.parameters['POLICY_OUT']['service-policy'])
        flow_template[10] = flow_template[10].replace('QOS_PROFILE', self.parameters['INTER']['POLICY_OUT'])
        flow_template[11] = flow_template[11].replace('SERVICE_POLICY', self.parameters['POLICY_OUT']['service-policy'])
        flow_template[11] = flow_template[11].replace('SHAPE_AVERAGE', self.parameters['POLICY_OUT']['shape average'])
        
        if self.parameters['FLOW_QUEUE'][' class MM'][0] == True:
            flow_template[1] = flow_template[1].replace('PERCENT_NUMBER', self.parameters['FLOW_QUEUE'][' class MM'][1])
        if self.parameters['FLOW_QUEUE'][' class PLATA'][0] == True:
            flow_template[2] = flow_template[2].replace('PERCENT_NUMBER', self.parameters['FLOW_QUEUE'][' class PLATA'][1])
        if self.parameters['FLOW_QUEUE'][' class ORO'][0] == True:
            flow_template[3] = flow_template[3].replace('PERCENT_NUMBER', self.parameters['FLOW_QUEUE'][' class ORO'][1])
        if self.parameters['FLOW_QUEUE'][' class PLATINO'][0] == True:
            flow_template[4] = flow_template[4].replace('PERCENT_NUMBER', self.parameters['FLOW_QUEUE'][' class PLATINO'][1])
        if self.parameters['FLOW_QUEUE'][' class VIDEO'][0] == True:
            flow_template[5] = flow_template[5].replace('PERCENT_NUMBER', self.parameters['FLOW_QUEUE'][' class VIDEO'][1])
        if self.parameters['FLOW_QUEUE'][' class BRONCE'][0] == True:
            flow_template[6] = flow_template[6].replace('PERCENT_NUMBER', self.parameters['FLOW_QUEUE'][' class BRONCE'][1])
        
        flow_template_bkp = flow_template
        flow_template = []
        for x in flow_template_bkp:
            flow_template.append(x) if not re.findall('PERCENT_NUMBER', x) else flow_template

        return flow_template
    
    def interface_service(self, inter_template, cabling_type):

        inter_template[0] = inter_template[0].replace('X/X/X', self.parameters['NEW_INTERFACE'])
        inter_template[5] = inter_template[5].replace('VPN_NAME', self.vpn)

        if self.parameters['INTER']['DESCRIP'] != "":
            inter_template[6] = inter_template[6].replace('NAME_SERVICE', self.parameters['INTER']['DESCRIP'])
        if self.parameters['INTER']['IP'] != "":
            inter_template[7] = inter_template[7].replace('NAME_SERVICE', self.parameters['INTER']['IP']+' '+self.parameters['INTER']['MASK'])
        if self.parameters['INTER']['IP_SEC'] != "":
            inter_template[8] = inter_template[8].replace('NAME_SERVICE', self.parameters['INTER']['IP_SEC']+' '+self.parameters['INTER']['MASK_SEC'])
        if self.parameters['INTER']['POLICY_IN'] != "":
            inter_template[9] = inter_template[9].replace('NAME_SERVICE', self.parameters['INTER']['POLICY_IN'])
        if self.parameters['INTER']['POLICY_OUT'] != "" and self.parameters['INTER']['POLICY_OUT'] == self.parameters['INTER']['POLICY_IN']:
            inter_template[10] = inter_template[10].replace('NAME_SERVICE', self.parameters['INTER']['POLICY_OUT'])
        if self.parameters['INTER']['POLICY_OUT'] != "" and self.parameters['INTER']['POLICY_OUT'] != self.parameters['INTER']['POLICY_IN']:
            inter_template[11] = inter_template[11].replace('NAME_SERVICE', self.parameters['INTER']['POLICY_OUT'])


        if self.parameters['INTER']['VLAN_ONE'] != "" and self.parameters['INTER']['VLAN_TWO'] != "":
            if cabling_type == 'fiber':
                inter_template[0] = inter_template[0].replace('VLANC', self.parameters['INTER']['VLAN_ONE']+self.parameters['INTER']['VLAN_TWO'])
                inter_template[4] = inter_template[4].replace('VLANUNO', self.parameters['INTER']['VLAN_ONE'])
                inter_template[4] = inter_template[4].replace('VLANDOS', self.parameters['INTER']['VLAN_TWO'])
                inter_template.remove(' Vlan-type dot1q VLANUNO\n')

            if cabling_type == 'electric':
                inter_template[0] = inter_template[0].replace('VLANC', self.parameters['INTER']['VLAN_TWO'])
                inter_template[2] = inter_template[2].replace('VLANUNO', self.parameters['INTER']['VLAN_TWO'])
                inter_template.remove(' encapsulation qinq-termination\n')
                inter_template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
                inter_template.remove(' arp broadcast enable\n')

        if self.parameters['INTER']['VLAN_ONE'] != "" and self.parameters['INTER']['VLAN_TWO'] == "":
            if cabling_type == 'fiber':
                inter_template[0] = inter_template[0].replace('VLANC', self.parameters['INTER']['VLAN_ONE'])
                inter_template[2] = inter_template[2].replace('VLANUNO', self.parameters['INTER']['VLAN_ONE'])
                inter_template.remove(' encapsulation qinq-termination\n')
                inter_template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
                inter_template.remove(' arp broadcast enable\n')

            if cabling_type == 'electric':
                inter_template[0] = inter_template[0].replace('.VLANC', "")
                inter_template.remove(' Vlan-type dot1q VLANUNO\n')
                inter_template.remove(' encapsulation qinq-termination\n')
                inter_template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
                inter_template.remove(' arp broadcast enable\n')

        if self.parameters['INTER']['VLAN_ONE'] == "" and self.parameters['INTER']['VLAN_TWO'] == "":
            inter_template[0] = inter_template[0].replace('.VLANC', '')
            inter_template.remove(' Vlan-type dot1q VLANUNO\n')
            inter_template.remove(' encapsulation qinq-termination\n')
            inter_template.remove(' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n')
            inter_template.remove(' arp broadcast enable\n')

        inter_template.remove(' shutdown\n') if self.parameters['INTER']['STATUS'] == "" else inter_template

        inter_template_bkp = inter_template
        inter_template = []
        for x in inter_template_bkp:
            if not re.findall('NAME_SERVICE', x):
                inter_template.append(x)

        return inter_template



