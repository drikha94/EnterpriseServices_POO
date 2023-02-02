class Template_residential:

    def __init__(self, residential_parameters, device_type):

        self.residential_parameters = residential_parameters
        self.physical_interface = residential_parameters['NEW_INTERFACE']
        self.device_type = device_type
        self.name_device = residential_parameters['NAME']
        self.id = residential_parameters['ID']
        self.eth_number = residential_parameters['NEW_ETH']

    def headers(self):

        headers_temp = [
            f'#################################\n',
            f'###### RESIDENTIAL SERVICE ######\n',
            f'#################################\n',
            f'#\n',
            f'#\n'
        ]
        return headers_temp
    
    def headers_service(self):

        name_of_device = [
            f'############## {self.name_device}\n',
            f'#\n'
        ]
        return name_of_device

    def templates_main(self):

        interface_temp = [
            f'interface Eth-TrunkETH_NUMBER\n',                  
            f'#\n',
            f' interface GigabitEthernet{self.physical_interface}\n',
            f' negotiation auto\n',
            f' description Conexion con {self.device_type} {self.name_device} ID: {self.id} Tipo: Acceso Fijo Eth-Trunk{self.eth_number}\n',
            f' undo shutdown\n',
            f' eth-trunk {self.eth_number}\n'
            f' #\n',
            f'interface Eth-Trunk{self.eth_number}\n',
            f' mtu 9216\n',
            f' description Conexion con {self.device_type} {self.name_device} Tipo: Acceso Fijo\n',
            f' statistic enable\n',
            f'#\n'
        ]
        return interface_temp

    def templates_qos(self):

        eth_main_qos = [
            f' trust upstream default\n',
            f' port-queue be lpq outbound\n',
            f' port-queue af1 wfq weight 5 port-wred QoS outbound\n',
            f' port-queue af2 wfq weight 10 port-wred QoS outbound\n',
            f' port-queue af3 wfq weight 30 port-wred QoS outbound\n',
            f' port-queue af4 pq shaping shaping-percentage 15 outbound\n',
            f' port-queue ef pq shaping shaping-percentage 15 outbound\n',
            f' port-queue cs6 pq shaping shaping-percentage 10 outbound\n',
            f' port-queue cs7 pq shaping shaping-percentage 5 outbound\n',
            f' qos phb disable\n',
            f' mode lacp-static\n',
            f'#\n'
        ]

        return eth_main_qos

    def template_speedy(self, vlan_speedy, name, num):

        speedy = [
            f'##### Speedy\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_speedy}\n',
            f' mtu 9086\n',
            f' description Conexion con {self.device_type} {name} Tipo: Trafico Internet\n',
            f' ipv6 enable\n',
            f' ipv6 address auto link-local\n',
            f' commit\n',
            f' user-vlan any-other\n',
            f' pppoe-server bind Virtual-Template 10\n',
            f' commit\n',
            f' bas\n',
            f'  access-type layer2-subscriber default-domain authentication wbc2\n',
            f'  nas-port-type xdsl\n',
            f'  roam-domain wbc2\n',
            f'  ipv6 nd ra unicast\n',
            f' #\n',
            f'#\n'
        ]

        if num > 0:
            speedy[6] = f' user-vlan 1 4094 qinq {vlan_speedy}\n'

        return speedy

    def voip_template(self, vlan_voip, name):

        voip = [
            f'##### VOIP\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_voip}\n',
            f' vlan-type dot1q {vlan_voip}\n',
            f' description Conexion con {self.device_type} {name} Tipo: Trafico VoIP\n',
            f' ip binding vpn-instance VOIP-IAD\n',
            f' ip address unnumbered interface LoopBack1002\n',
            f' statistic enable\n',
            f' arp expire-time 60\n',
            f' arp learning strict force-disable\n',
            f' dhcp select relay\n',
            f' ip relay address 172.19.3.10\n',
            f' ip relay address 172.19.4.10\n',
            f' dhcp snooping enable\n',
            f' dhcp snooping alarm dhcp-reply enable\n',
            f' #\n',
            f'#\n'
        ]

        return voip

    def gid_template(self, vlan_gid, name, route):

        gid = [
            f'##### gid1\n'
            f'#\n'
            f'interface Eth-Trunk{self.eth_number}.{vlan_gid}\n',               
            f' vlan-type dot1q {vlan_gid}\n',
            f' description Conexion con {self.device_type} {name} Tipo: Gestion GPON\n',
            f' ip binding vpn-instance gid1\n',
            f' ip address unnumbered interface LoopBack184\n',
            f' statistic enable\n',
            f'#\n'
        ]
        static = f'ip route-static vpn-instance gid1 IP_DES MASK_DES Eth-Trunk{self.eth_number}.{vlan_gid} IP_DES\n'

        for x in range(len(route)):
            gid.append(static.replace('IP_DES', route[x][0]).replace('MASK_DES', route[x][1]))
        
        gid.append('#\n')

        return gid

    def modems_template(self, vlan_modems, name):

        g_modems = [
            f'##### Enterprise Management\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_modems}\n',                   
            f' vlan-type dot1q {vlan_modems}\n',
            f' description Conexión con {self.device_type} {name} Tipo: Gestion Modems G.SHDSL\n',
            f' ip binding vpn-instance GESTION_NB\n',
            f' ip address 172.24.X.X 255.255.254.0\n',      
            f' statistic enable\n'
            f'#\n'
        ]
        return g_modems
    
    def enterprise_template(self, vlan_enterprise, name):

        traffic_emp = [
            f'##### Enterprise Traffic\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_enterprise}\n',
            f' vlan-type dot1q {vlan_enterprise}\n',
            f' description FRT:{name}_{self.device_type}#DA:FTTH\n',
            f' statistic enable\n'
            f'#\n'
        ]
        return traffic_emp
    
    def ngn_traffic_template(self, vlan_ngn_t,name,ip_address):

        ngn_traffic = [
            f'##### NGN Traffic\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_ngn_t}\n',
            f' vlan-type dot1q {vlan_ngn_t}\n',
            f' description Conexion de {self.device_type} {name} Tipo: Trafico NGN\n',
            f' ip binding vpn-instance NGN\n',
            f' ip address {ip_address}\n',
            f' statistic enable\n',
            f'#\n'
        ]
        return ngn_traffic
    
    def ngn_senialization_template(self, vlan_ngn_s, name, ip_address):

        ngn_senialization = [
            f'##### NGN Senialization\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_ngn_s}\n',
            f' vlan-type dot1q {vlan_ngn_s}\n',
            f' description Conexion de {self.device_type} {name} Tipo: Trafico Senializacion\n',
            f' ip binding vpn-instance NGN\n',
            f' ip address {ip_address}\n',
            f'#\n'
        ]

        return ngn_senialization
    
    def iptv_multi_template(self, vlan_multi, name, ip_address):

        iptv_multicast = [
            f'##### IPTV Multicast\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_multi}\n',
            f' vlan-type dot1q {vlan_multi}\n',
            f' description Conexion con {self.device_type} {name} Tipo: IPTV-MULTICAST\n',
            f' ip binding vpn-instance IPTV-MULTICAST-NG\n',
            f' ip address {ip_address}\n',
            f' statistic enable\n',
            f' pim sm\n',
            f' igmp enable\n',
            f' igmp ssm-mapping enable\n',
            f'#\n'
        ]
        return iptv_multicast

    def iptv_uni_template(self, vlan_uni, name, ip_address, routes):

        iptv_unicast = [
            f'##### IPTV Unicast\n',
            f'#\n',
            f'interface Eth-Trunk{self.eth_number}.{vlan_uni}\n',
            f' vlan-type dot1q {vlan_uni}\n',
            f' description Conexion con {self.device_type} {name} Tipo: IPTV-UNICAST\n',
            f' ip binding vpn-instance IPTV-UNICAST\n',
            f' ip address {ip_address[0]} {ip_address[1]}\n',
            f' arp learning strict force-disable\n',
            f'#\n'
        ]
        static = f'ip route-static vpn-instance IPTV-UNICAST IP_DES MASK_DES IP_PEER\n'
        for x in range(len(routes)):
            iptv_unicast.append(static.replace('IP_DES', routes[x][0]).replace('MASK_DES', routes[x][1]).replace('IP_PEER', routes[x][2]))
            
        iptv_unicast.append('#\n')

        return iptv_unicast