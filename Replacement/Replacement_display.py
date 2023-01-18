import re
class Display_template:

    def __init__(self, parameters, path_display, display_template):

        self.parameters = parameters
        self.path_display = path_display
        self.display_template = display_template
        self.vpn = 'INFOINTERNET' if self.parameters['INTER']['VPN'] == "" else self.parameters['INTER']['VPN']
        self.add_display = open(self.path_display, "a")

    def display_command(self):

        template = []
        command = self.parameters['DISPLAY_COMMAND']

        def headers():
            if self.parameters['INTER']['REF'] != "":
                self.display_template[0] = self.display_template[0].replace('TO_REPLACE', self.parameters['INTER']['REF'])
            else:
                self.display_template[0] = self.display_template[0].replace('REF:TO_REPLACE', self.parameters['INTER']['DESCRIP'])

        def check_power_arp():
            self.display_template[2] = self.display_template[2] + command['interface'] + command['vlan'] + '\n'
            inter = command['interface'].replace('GigabitEthernet', '').replace('Eth-Trunk', '')
            self.display_template[3] = self.display_template[3] + inter + command['vlan'] + '\n'

        def add_ping():
            if self.parameters['INTER']['IP'] != "":
                self.display_template[4] = self.display_template[4].replace('IP_MAIN', self.parameters['INTER']['IP'])

            if self.parameters['ROUTES'] != []:
                for x in range(len(self.parameters['ROUTES'])):
                    route = self.parameters['ROUTES'][x].split()
                    self.display_template.insert(5+x, self.display_template[4])
                    self.display_template[5+x] = self.display_template[5+x].replace('IP_REMOTE', route[0])

            if self.parameters['BGP']['PEER'] != "":
                self.display_template[4] = self.display_template[4].replace('IP_REMOTE', self.parameters['BGP']['PEER'])

            if self.parameters['BGP']['PEER'] == "" and self.parameters['ROUTES'] != []:
                peer = self.parameters['ROUTES'][0].split()
                self.display_template[4] = self.display_template[4].replace('IP_REMOTE', peer[2])
        
        
        def routing_table():

            for x in self.display_template:
                x = x.replace('VPN_NAME', self.vpn)
                if self.parameters['BGP']['STATUS'] == True:
                    if self.parameters['BGP']['PEER'] != "":
                        x = x.replace('IP_REMOTE', self.parameters['BGP']['PEER'])
                    template.append(x)
                else:
                    if not re.findall('routing-table', x):
                        template.append(x)
            
            self.add_display.write("".join(template))

        headers(), check_power_arp(), add_ping(), routing_table()
        
