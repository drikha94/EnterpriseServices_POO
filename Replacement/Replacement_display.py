import re
class Display_template:

    def __init__(self, parameters, path_display, display_template):

        self.parameters = parameters
        self.path_display = path_display
        self.display_template = display_template
        self.vpn = 'INFOINTERNET' if self.parameters['INTER']['VPN'] == "" else self.parameters['INTER']['VPN']
        self.add_display = open(self.path_display, "a")

    def display_command(self):

        new_template = []
        peer, routes, ref = self.parameters['BGP']['PEER'], self.parameters['ROUTES'], self.parameters['INTER']['REF']
        description, ip = self.parameters['INTER']['DESCRIP'], self.parameters['INTER']['IP']
        command = self.parameters['DISPLAY_COMMAND']

        headers = f'############ REF:{ref}\n' if ref != "" else f'############ {description}\n'
        new_template.append(headers)
        new_template.append('#\n')

        check_power = 'display interface brief ' + command['interface'] + command['vlan'] + '\n'
        new_template.append(check_power)

        inter = command['interface'].replace('GigabitEthernet', '').replace('Eth-Trunk', '')
        check_arp = 'display arp all | inc ' +  inter + command['vlan'] + '\n'
        new_template.append(check_arp)

        if peer != "":
            ping = f'ping -vpn-instace {self.vpn} -a {ip} {peer}\n'
            adv_routes = f'display bgp vpnv4 vpn-instance {self.vpn} routing-table peer {peer} advertised-routes\n'
            rcv_routes = f'display bgp vpnv4 vpn-instance {self.vpn} routing-table peer {peer} accepted-routes\n'
            new_template.append(ping)
            new_template.append(adv_routes)
            new_template.append(rcv_routes)
        
        if routes != []:
            for x in range(len(routes)):
                route = routes[x].split()

                command = f'ping -vpn-instace {self.vpn} -a {ip} {route[0]}\n'
                command_peer = f'ping -vpn-instace {self.vpn} -a {ip} {route[2]}\n'

                if command_peer not in new_template:
                    new_template.append(command_peer)
                new_template.append(command)
        new_template.append('#\n')
        new_template.append('#\n')
            
        self.add_display.write("".join(new_template))

        
