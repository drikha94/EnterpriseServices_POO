
class Management_template:

    def __init__(self, parameters):

        self.new_interface = parameters
        self.description = parameters
        self.loopback = parameters
        self.id = parameters
        self.adred = parameters
        self.description_service = parameters

    def switch_mgmt(self):

        switch = [
        f'interface GigabitEthernet{self.new_interface}.4002\n',
        f' vlan-type dot1q 4002\n',
        f' description Conexion con {self.description} Tipo: Gestion S2300\n',
        f' ip binding vpn-instance Mgmt-HL5\n',
        f' ip address unnumbered interface Loopback4002\n',
        f' statistic enable\n',
        f' dhcp select relay\n',
        f' ip relay address 10.105.10.109\n',
        f'#\n',
        f'interface GigabitEthernet{self.new_interface}.4000\n',
        f' vlan-type dot1q 4000\n',
        f' description Conexion con {self.description} Tipo: Gestion S2300\n',
        f' ip binding vpn-instance Mgmt-HL5\n',
        f' ip address unnumbered interface Loopback4000\n',
        f' statistic enable\n',
        f'#\n',
        f'ip route-static vpn-instance Mgmt-HL5 {self.loopback} 255.255.255.255 GigabitEthernet{self.new_interface}.4000 {self.loopback}\n',
        f'#\n',
        f'interface GigabitEthernet{self.new_interface}\n',
        f' description Conexion con {self.description} ID: {self.id} ADRED: {self.adred} Tipo: Acceso\n',
        f'#\n',
        f'#####\n',
        f'#\n'
        ]

    def tmarc_electric_mgmt(self):
        
        tmarc_electric = [
        f'interface GigabitEthernet{self.new_interface}\n',
        f' undo shutdown\n',
        f' description Conexion con {self.description} Tipo: Acceso (T-Marc)\n',
        f'#\n',
        f'######\n',
        f'#\n'
        ]

    def tmarc_fiber_mgmt(self):

        tmarc_fiber = [
        f'interface GigabitEthernet{self.new_interface}\n',
        f' undo shutdown\n',
        f' description Conexion con {self.description} Tipo: Acceso (T-Marc)\n',
        f'#\n',
        f'interface GigabitEthernet{self.new_interface}.999\n',
        f' vlan-type dot1q 999\n',
        f' description GESTION:TMARC {self.description} (T-Marc)\n',
        f' ip binding vpn-instance TELCO_TMARC\n',
        f' ip address unnumbered interface LoopBack 999\n',
        f' statistic enable\n',
        f'#\n',
        f'ip route-static vpn-instance TELCO_TMARC {self.loopback} 255.255.255.255 GigabitEthernet{self.new_interface}.999 {self.loopback} description *** {self.description} ***\n',
        f'#\n',
        f'######\n',
        f'#\n'
        ]

    def atn_mgmt(self):

        atn = [
        f'interface GigabitEthernet{self.new_interface}\n',
        f' description Conexion con {self.description} ID: {self.id} ADRED: {self.adred} Tipo: Acceso\n',
        f'#\n',
        f' interface GigabitEthernet{self.new_interface}.4002\n',
        f' vlan-type dot1q 4002\n',
        f' description Conexion con {self.description} Tipo: Acceso\n',
        f' ip binding vpn-instance Mgmt-HL5\n',
        f' ip address unnumbered interface Loopback4002\n',
        f' statistic enable\n',
        f' dhcp select relay\n',
        f' ip relay address 10.105.10.109\n',
        f' dhcp snooping enable\n',
        f'#\n',
        f'#####\n',
        f'#\n'
        ]

    def core_mgmt(self):

        core = [
        f'interface GigabitEthernet{self.new_interface}\n',
        f' description Conexion con {self.description_service}\n',
        f'#\n',
        f'#####\n',
        f'#\n'
        ]
