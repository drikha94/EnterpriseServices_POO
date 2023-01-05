import re

class Service_template:

    def __init__(self, parameters):

        self.parameters = parameters
        self.vpn = parameters['INTER']['VPN']
        self.peer = parameters['BGP']['PEER']
        self.as_number = parameters['BGP']['ATTRIBUTES']['as-number']
        self.description = parameters['BGP']['ATTRIBUTES']['description']
        self.load_balancing = parameters['BGP']['ATTRIBUTES']['maximum load-balancing ibgp']
        self.route_limit = parameters['BGP']['ATTRIBUTES']['route-limit']
        self.password = parameters['BGP']['ATTRIBUTES']['password cipher']
        self.ebgp_max_hop = parameters['BGP']['ATTRIBUTES']['ebgp-max-hop']
        self.allow_as_loop = parameters['BGP']['ATTRIBUTES']['allow-as-loop']
        self.route_interval = parameters['BGP']['ATTRIBUTES']['route-update-interval']
        self.route_reflector = parameters['BGP']['ATTRIBUTES']['reflect-client']
        self.route_rip = parameters['BGP']['ATTRIBUTES']['import-route rip']

    def bgp_service(self):

        """CUALQUIER COMANDO QUE SE QUIERA AGREGAR ES NECESARIO AGREGARLO TAMBIEN EN EL ARCHIVO Establish_Parameters.py
        EN EL MISMO ORDEN EN EL QUE SE AGREGE EN EL TEMPLATE, CON SU RESPECTIVA CONFIRMACION BOOLEANA"""

        bgp = [
        f'bgp 22927\n', 
        f' ipv4-family vpn-instance {self.vpn}\n',
        f' import-route direct\n',
        f' import-route static\n',
        f' import-route rip {self.route_rip[1]}\n',
        f' maximum load-balancing ibgp {self.load_balancing[1]}\n',
        f' peer {self.peer} as-number {self.as_number[1]}\n',
        f' peer {self.peer} description {self.description[1]}\n',
        f' peer {self.peer} advertise-community\n',
        f' peer {self.peer} keep-all-routes\n',
        f' peer {self.peer} substitute-as\n',
        f' peer {self.peer} fake-as 10834\n',
        f' peer {self.peer} route-limit {self.route_limit[1]}\n',
        f' peer {self.peer} default-route-advertise\n',
        f' peer {self.peer} password cipher {self.password[1]}\n',
        f' peer {self.peer} ebgp-max-hop {self.ebgp_max_hop[1]}\n',
        f' peer {self.peer} allowas-in {self.allow_as_loop[1]}\n',
        f' peer {self.peer} route-update-interval {self.route_interval[1]}\n',
        f' peer {self.peer} reflect-client\n',
        f' peer {self.peer} enable\n',
        ]

        confirmation, bgp_service = [], []
        for x in self.parameters['BGP']['ATTRIBUTES'].values():
            confirmation.append(x[0])
        
        for x in range(len(bgp)):
            if confirmation[x] == True:
                bgp_service.append(bgp[x]) 

            
        return bgp_service

        #return bgp_service

