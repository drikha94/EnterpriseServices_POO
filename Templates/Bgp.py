import re

class Service_template:

    def __init__(self, parameters):

        self.parameters = parameters
        self.vpn = parameters['INTER']['VPN'] if parameters['INTER']['VPN'] != "" else 'INFOINTERNET'

    def policy_service(self):

        enlace = self.parameters['INTER']['POLICY_IN']
        policy_in = self.parameters['POLICY_IN']

        policy_template = [
            f'traffic classifier default\n',
            f' if-match any\n',
            f' commit\n',
            f' quit\n',
            f'#\n',
            f'traffic behavior {enlace}\n',
            f' car cir number_one ', f'cbs number_two ', f'pbs number_tree green pass red discard', '\n'
            f'#\n', 
            f' traffic policy {enlace}\n',
            f' undo share-mode\n', 
            f' statistics enable\n', 
            f' classifier default behavior {enlace}\n',
            f'#\n',
            f'#'
        ]
        print(policy_in)
        if len(policy_in) == 1:
            policy_template[6] = policy_template[6].replace('number_one', policy_in[0])
            policy_template.remove('cbs number_two ')
            policy_template.remove('pbs number_tree green pass red discard')

        if len(policy_in) == 2:
            policy_template[6] = policy_template[6].replace('number_one', policy_in[0])
            policy_template[7] = policy_template[7].replace('number_two', policy_in[1])
            policy_template.pop(8)

        if len(policy_in) == 3:
            policy_template[6] = policy_template[6].replace('number_one', policy_in[0])
            policy_template[7] = policy_template[7].replace('number_two', policy_in[1])
            policy_template[8] = policy_template[8].replace('number_tree', policy_in[2])

        return policy_template
       
    def vpn_service(self):
       
        description = self.parameters['VPN']['DESCRIP']
        rd = self.parameters['VPN']['RD']
        rte = self.parameters['VPN']['RTE']
        rti = self.parameters['VPN']['RTI']

        vpn_template = [
        f'ip vpn-instance {self.vpn}\n',
        f' description ### {description} ###\n',
        f' ipv4-family\n',
        f'  route-distinguisher {rd}\n',
        f'  vpn-target rte export-extcommunity\n',
        f'  vpn-target rti import-extcommunity\n',
        f'  apply-label per-instance\n',
        f'#\n',
        f'#\n'
        ]
        
        def target(vpn_target, to_replace, to_insert, num):
            for x in range(len(vpn_target)):
                vpn_template[num] = vpn_template[num].replace(to_replace, vpn_target[x])
                if x < len(vpn_target):
                    vpn_template.insert(num+1, to_insert)
                    num += 1
        
        target(rte, 'rte', '  vpn-target rte export-extcommunity\n', 4)
        target(rti, 'rti', '  vpn-target rti import-extcommunity\n', vpn_template.index('  vpn-target rti import-extcommunity\n'))
        vpn_template.remove('  vpn-target rte export-extcommunity\n')
        vpn_template.remove('  vpn-target rti import-extcommunity\n')

        return vpn_template

    def bgp_service(self):

        """CUALQUIER COMANDO QUE SE QUIERA AGREGAR ES NECESARIO AGREGARLO TAMBIEN EN EL 
        ARCHIVO Establish_Parameters.py EN EL MISMO ORDEN EN EL QUE SE AGREGE EN EL TEMPLATE, 
        CON SU RESPECTIVA CONFIRMACION BOOLEANA"""
        
        peer = self.parameters['BGP']['PEER']
        as_number = self.parameters['BGP']['ATTRIBUTES']['as-number']
        description = self.parameters['BGP']['ATTRIBUTES']['description']
        load_balancing = self.parameters['BGP']['ATTRIBUTES']['maximum load-balancing ibgp']
        route_limit = self.parameters['BGP']['ATTRIBUTES']['route-limit']
        password = self.parameters['BGP']['ATTRIBUTES']['password cipher']
        ebgp_max_hop = self.parameters['BGP']['ATTRIBUTES']['ebgp-max-hop']
        allow_as_loop = self.parameters['BGP']['ATTRIBUTES']['allow-as-loop']
        route_interval = self.parameters['BGP']['ATTRIBUTES']['route-update-interval']
        route_rip = self.parameters['BGP']['ATTRIBUTES']['import-route rip']

        bgp_template = [
        f'bgp 22927\n', 
        f' ipv4-family vpn-instance {self.vpn}\n',
        f' import-route direct\n',
        f' import-route static\n',
        f' import-route rip {route_rip[1]}\n',
        f' maximum load-balancing ibgp {load_balancing[1]}\n',
        f' peer {peer} as-number {as_number[1]}\n',
        f' peer {peer} description {description[1]}\n',
        f' peer {peer} advertise-community\n',
        f' peer {peer} keep-all-routes\n',
        f' peer {peer} substitute-as\n',
        f' peer {peer} fake-as 10834\n',
        f' peer {peer} route-limit {route_limit[1]}\n',
        f' peer {peer} default-route-advertise\n',
        f' peer {peer} password cipher {password[1]}\n',
        f' peer {peer} ebgp-max-hop {ebgp_max_hop[1]}\n',
        f' peer {peer} allowas-in {allow_as_loop[1]}\n',
        f' peer {peer} route-update-interval {route_interval[1]}\n',
        f' peer {peer} reflect-client\n',
        f' peer {peer} enable\n',
        ]

        confirmation, bgp_service = [], []
        for x in self.parameters['BGP']['ATTRIBUTES'].values():
            confirmation.append(x[0])

        for x in range(len(bgp_template)):
            if confirmation[x] == True:
                bgp_service.append(bgp_template[x]) 
 
        return bgp_service

    def flow_queue(self):

        qos_profile = self.parameters['INTER']['POLICY_OUT']
        service_policy = self.parameters['POLICY_OUT']['service-policy']
        shape_average = self.parameters['POLICY_OUT']['shape average']
        class_service = self.parameters['FLOW_QUEUE']

        flow_template = [
        f'flow-queue {service_policy}\n',  
        f'  queue ef pq shaping shaping-percentage EF_PERCENT\n',
        f'  queue AF1 wfq weight xx\n',
        f'  queue AF2 wfq weight xx\n',
        f'  queue AF3 wfq weight xx\n',
        f'  queue AF4 wfq weight xx\n',
        f'  queue BE wfq weight xx\n',
        f'  quit\n',
        f'commit\n',
        f'#\n',
        f'qos-profile {qos_profile}\n',
        f' user-queue cir {shape_average} flow-queue {service_policy}\n',
        f'#\n',
        f'#\n'
        ]
        print(self.parameters)
        if class_service[' class MM'][0] == True:
            flow_template[1] = flow_template[1].replace('EF_PERCENT', class_service[' class MM'][1])
        else:
            flow_template.remove('  queue ef pq shaping shaping-percentage EF_PERCENT\n')

        if class_service[' class PLATA'][0] == True:
            flow_template[2] = flow_template[2].replace('xx', class_service[' class PLATA'][1])
        else:
            flow_template.remove('  queue AF1 wfq weight xx\n')

        if class_service[' class ORO'][0] == True:
            flow_template[3] = flow_template[3].replace('xx', class_service[' class ORO'][1])
        else:
            flow_template.remove('  queue AF2 wfq weight xx\n')

        print(flow_template)
        if class_service[' class PLATINO'][0] == True:
            flow_template[4] = flow_template[4].replace('xx', class_service[' class PLATINO'][1])
        else:
            flow_template.remove('  queue AF3 wfq weight xx\n')

        if class_service[' class VIDEO'][0] == True:
            flow_template[5] = flow_template[5].replace('xx', class_service[' class VIDEO'][1])
        else:
            flow_template.remove('  queue AF4 wfq weight xx\n')
        
        if class_service[' class BRONCE'][0] == True:
            flow_template[6] = flow_template[6].replace('xx', class_service[' class VIDEO'][1])
        else:
            flow_template.remove('  queue BE wfq weight xx\n')

        


        return flow_template




