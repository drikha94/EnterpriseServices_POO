import re

class Management_template:

    def __init__(self, parameters, path_script, headers_template):

        self.interface_type = 'Eth-Trunk' if not re.findall('/', parameters['NEW_INTERFACE']) else 'GigabitEthernet'
        self.new_interface = parameters['NEW_INTERFACE']
        self.description = parameters['MANAGEMENT_DATA']['device_name']
        self.loopback = parameters['MANAGEMENT_DATA']['mgmt_ip']
        self.id = parameters['MANAGEMENT_DATA']['ID']
        self.adred = parameters['MANAGEMENT_DATA']['ADRED']
        self.description_service = parameters['INTER']['DESCRIP']
        self.path_script = path_script
        self.add_script = open(self.path_script, "a")
        self.headers = headers_template
    
    def add_headers(self):
        self.add_script.write(self.headers)

    def switch_mgmt(self):

        switch = [
        f'########## {self.description}\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}.4002\n',
        f' vlan-type dot1q 4002\n',
        f' description Conexion con {self.description} Tipo: Gestion S2300\n',
        f' ip binding vpn-instance Mgmt-HL5\n',
        f' ip address unnumbered interface Loopback4002\n',
        f' statistic enable\n',
        f' dhcp select relay\n',
        f' ip relay address 10.105.10.109\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}.4000\n',
        f' vlan-type dot1q 4000\n',
        f' description Conexion con {self.description} Tipo: Gestion S2300\n',
        f' ip binding vpn-instance Mgmt-HL5\n',
        f' ip address unnumbered interface Loopback4000\n',
        f' statistic enable\n',
        f'#\n',
        f'ip route-static vpn-instance Mgmt-HL5 {self.loopback} 255.255.255.255 {self.interface_type}{self.new_interface}.4000 {self.loopback}\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}\n',
        f' description Conexion con {self.description} ID: {self.id} ADRED: {self.adred} Tipo: Acceso\n',
        f'#\n',
        f'#\n'
        ]
        self.add_script.write("".join(switch.copy()))

    def tmarc_electric_mgmt(self):
        
        tmarc_electric = [
        f'########## {self.description}\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}\n',
        f' undo shutdown\n',
        f' description Conexion con {self.description} Tipo: Acceso (T-Marc)\n',
        f'#\n',
        f'#\n'
        ]
        self.add_script.write("".join(tmarc_electric.copy()))

    def tmarc_fiber_mgmt(self):

        tmarc_fiber = [
        f'########## {self.description}\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}\n',
        f' undo shutdown\n',
        f' description Conexion con {self.description} Tipo: Acceso (T-Marc)\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}.999\n',
        f' vlan-type dot1q 999\n',
        f' description GESTION:TMARC {self.description} (T-Marc)\n',
        f' ip binding vpn-instance TELCO_TMARC\n',
        f' ip address unnumbered interface LoopBack 999\n',
        f' statistic enable\n',
        f'#\n',
        f'ip route-static vpn-instance TELCO_TMARC {self.loopback} 255.255.255.255 {self.interface_type}{self.new_interface}.999 {self.loopback} description *** {self.description} ***\n',
        f'#\n',
        f'#\n'
        ]
        self.add_script.write("".join(tmarc_fiber.copy()))

    def atn_mgmt(self):

        atn = [
        f'########## {self.description}\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}\n',
        f' description Conexion con {self.description} ID: {self.id} ADRED: {self.adred} Tipo: Acceso\n',
        f'#\n',
        f' interface {self.interface_type}{self.new_interface}.4002\n',
        f' vlan-type dot1q 4002\n',
        f' description Conexion con {self.description} Tipo: Acceso\n',
        f' ip binding vpn-instance Mgmt-HL5\n',
        f' ip address unnumbered interface Loopback4002\n',
        f' statistic enable\n',
        f' dhcp select relay\n',
        f' ip relay address 10.105.10.109\n',
        f' dhcp snooping enable\n',
        f'#\n',
        f'#\n'
        ]
        self.add_script.write("".join(atn.copy()))

    def core_mgmt(self):

        core = [
        f'########## {self.description}\n',
        f'#\n',
        f'interface {self.interface_type}{self.new_interface}\n',
        f' description Conexion con {self.description_service}\n',
        f'#\n',
        f'#\n'
        ]
        self.add_script.write("".join(core.copy()))
