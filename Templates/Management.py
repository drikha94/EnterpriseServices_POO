
class Management_template:

    def __init__(self, parameters):

        self.new_interface = parameters
        self.description = parameters
        self.loopback = parameters
        self.id = parameters
        self.adred = parameters
        self.description_service = parameters

    def switch_mgmt(self):

        switch = f"""
interface GigabitEthernet{self.new_interface}.4002
 vlan-type dot1q 4002
 description Conexion con {self.description} Tipo: Gestion S2300
 ip binding vpn-instance Mgmt-HL5
 ip address unnumbered interface Loopback4002
 statistic enable
 dhcp select relay
 ip relay address 10.105.10.109
#
interface GigabitEthernet{self.new_interface}.4000
 vlan-type dot1q 4000
 description Conexion con {self.description} Tipo: Gestion S2300
 ip binding vpn-instance Mgmt-HL5
 ip address unnumbered interface Loopback4000
 statistic enable
#
ip route-static vpn-instance Mgmt-HL5 {self.loopback} 255.255.255.255 GigabitEthernet{self.new_interface}.4000 {self.loopback}
#
interface GigabitEthernet{self.new_interface}
 description Conexion con {self.description} ID: {self.id} ADRED: {self.adred} Tipo: Acceso
#
#####
#

"""

    def tmarc_electric_mgmt(self):
        
        tmarc_electric = f"""
interface GigabitEthernet{self.new_interface}
 undo shutdown
 description Conexion con {self.description} Tipo: Acceso (T-Marc)
#
######
#

"""
    def tmarc_fiber_mgmt(self):

        tmarc_fiber = f"""
interface GigabitEthernet{self.new_interface}
 undo shutdown
 description Conexion con {self.description} Tipo: Acceso (T-Marc)
#
interface GigabitEthernet{self.new_interface}.999
 vlan-type dot1q 999
 description GESTION:TMARC {self.description} (T-Marc)
 ip binding vpn-instance TELCO_TMARC
 ip address unnumbered interface LoopBack 999
 statistic enable
#
ip route-static vpn-instance TELCO_TMARC {self.loopback} 255.255.255.255 GigabitEthernet{self.new_interface}.999 {self.loopback} description *** {self.description} ***
#
######
#

"""

    def atn_mgmt(self):

        atn = f"""
interface GigabitEthernet{self.new_interface}
 description Conexion con {self.description} ID: {self.id} ADRED: {self.adred} Tipo: Acceso
#
 interface GigabitEthernet{self.new_interface}.4002
 vlan-type dot1q 4002
 description Conexion con {self.description} Tipo: Acceso
 ip binding vpn-instance Mgmt-HL5
 ip address unnumbered interface Loopback4002
 statistic enable
 dhcp select relay
 ip relay address 10.105.10.109
 dhcp snooping enable
#
#####
#
"""
    def core_mgmt(self):

        core = f"""
interface GigabitEthernet{self.new_interface}
 description Conexion con {self.description_service}
#
#####
#
"""

template_management_obj = Management_template()