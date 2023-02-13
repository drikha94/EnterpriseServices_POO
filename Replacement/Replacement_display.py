import re
class Display_template:

    def __init__(self, parameters, path_display):

        self.parameters = parameters
        self.path_display = path_display
        self.add_display = open(self.path_display, "a")

    def display_command(self):

        new_interface = self.parameters['NEW_INTERFACE']
        vpn = 'INFOINTERNET' if self.parameters['INTER']['VPN'] == "" else self.parameters['INTER']['VPN']
        new_template = []
        peer, routes, ref = self.parameters['BGP']['PEER'], self.parameters['ROUTES'], self.parameters['INTER']['REF']
        description, ip = self.parameters['INTER']['DESCRIP'], self.parameters['INTER']['IP']
        command = self.parameters['DISPLAY_COMMAND']

        headers = f'#### REF:{ref}\n' if ref != "" else f'############ {description}\n'
        new_template.append(headers)
        new_template.append('#\n')

        if command['vlan'] != "":
            check_power = 'display interface brief ' + command['interface'] + new_interface + '.' + command['vlan'] + '\n'
        else:
            check_power = 'display interface brief ' + command['interface'] + new_interface + '\n'
        new_template.append(check_power)

        inter = command['interface'].replace('GigabitEthernet', '').replace('Eth-Trunk', '')
        if command['vlan'] != "":
            check_arp = 'display arp all | inc ' +  inter + new_interface + '.' +command['vlan'] + '\n'
        else:
            check_arp = 'display arp all | inc ' +  inter + new_interface + '\n'
        new_template.append(check_arp)

        if peer != "":
            ping = f'ping -vpn-instace {vpn} -a {ip} {peer}\n'
            bgp_status = f'display bgp vpnv4 vpn-instance {vpn} peer | inc {peer}\n'
            adv_routes = f'display bgp vpnv4 vpn-instance {vpn} routing-table peer {peer} advertised-routes | inc Total\n'
            rcv_routes = f'display bgp vpnv4 vpn-instance {vpn} routing-table peer {peer} accepted-routes | inc Total\n'
            new_template.append(ping)
            new_template.append(bgp_status)
            new_template.append(adv_routes)
            new_template.append(rcv_routes)
        
        if routes != []:
            for x in range(len(routes)):
                route = routes[x].split()

                command = f'ping -vpn-instace {vpn} -a {ip} {route[0]}\n'
                command_peer = f'ping -vpn-instace {vpn} -a {ip} {route[2]}\n'

                if command_peer not in new_template:
                    new_template.append(command_peer)
                new_template.append(command)
        new_template.append('#\n')
        new_template.append('#\n')
            
        self.add_display.write("".join(new_template))

    def display_residential_cmd(self):
        
        eth = self.parameters['NEW_ETH']
        speedy = self.parameters['VLAN']['TRAFFIC INTERNET']
        voip = self.parameters['VLAN']['TRAFFIC VOIP']
        gid1 = self.parameters['VLAN']['GESTION GID1']
        name = self.parameters['NAME']
        new_template = []
        headers = f'############ {name}\n'
        new_template.append(headers)
        new_template.append('#\n')

        if speedy != []:
            new_template.append('#### Check speedy\n')
            new_template.append('#\n')
            for x in range(len(speedy)):
                new_template.append(f'display access-user pevlan {speedy[x][0]}\n')
            new_template.append('#\n')
        
        if voip != []:
            new_template.append('#### Check voip\n')
            new_template.append('#\n')
            for x in range(len(voip)):
                new_template.append(f'display arp interface Eth-Trunk{eth}.{voip[x][0]}\n')
            new_template.append('#\n')
        
        self.add_display.write("".join(new_template))

    