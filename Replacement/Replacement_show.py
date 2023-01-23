import re
class Show_template:

    def __init__(self, parameters, path_show, pattern):

        self.parameters = parameters
        self.path_show = path_show
        self.add_show = open(self.path_show, "a")
        self.patterns = pattern
    
    def show_command(self):

        vpn, peer, routes = self.parameters['INTER']['VPN'], self.parameters['BGP']['PEER'], self.parameters['ROUTES']
        ref, description, inter = self.parameters['INTER']['REF'], self.parameters['INTER']['DESCRIP'], self.parameters['OLD_INTERFACE']
        new_template = []

        headers = f'############ REF:{ref}\n' if ref != "" else f'############ {description}\n'
        new_template.append(headers)
        new_template.append('#\n')

        status_inter = f'show {inter}\n'
        new_template.append(status_inter)

        if peer != "":
            if vpn != "":
                command_ping_peer = f'ping vrf {vpn} {peer}\n'
            else:
                command_ping_peer = f'ping {peer}\n'
            
            if self.patterns['id'] == 1:
                if vpn != "":
                    command_bgp_one = f'show bgp vpnv4 unicast vrf {vpn} neighbors {peer} routes\n'
                    command_bgp_two = f'show bgp vpnv4 unicast vrf {vpn} neighbors {peer} advertised-routes\n'
                else:
                    command_bgp_one = f'show bgp vpnv4 unicast all neighbors {peer} routes\n'
                    command_bgp_two = f'show bgp vpnv4 unicast all neighbors {peer} advertised-routes\n'

            if self.patterns['id'] == 2:
                if vpn != "":
                    command_bgp_one = f'show bgp vrf {vpn} neighbors {peer} routes\n'
                    command_bgp_two = f'show bgp vrf {vpn} neighbors {peer} advertised-routes\n'
                else:
                    command_bgp_one = f'show bgp vpnv4 unicast neighbors {peer} routes\n'
                    command_bgp_two = f'show bgp vpnv4 unicast neighbors {peer} advertised-routes\n'


            new_template.append(command_ping_peer)
            new_template.append(command_bgp_one)
            new_template.append(command_bgp_two)

        if routes != []:
            for x in range(len(self.parameters['ROUTES'])):
                route = routes[x].split()

                if vpn != "":
                    command = f'ping vrf {vpn} {route[0]}\n'
                    command_peer = f'ping vrf {vpn} {route[2]}\n'
                else:
                    command = f'ping {route[0]}\n'
                    command_peer = f'ping {route[2]}\n'

                if command_peer not in new_template:
                    new_template.append(command_peer)
                new_template.append(command)
        new_template.append('#\n')
        new_template.append('#\n')

        self.add_show.write("".join(new_template))
