class Version:

    def check_version(self, core_list):

        core_list = core_list
        ver = ""
        uno_pruebav = "".join(filter(lambda x: "address-family ipv4 vrf" in x, core_list))
        dos_pruebav = "".join(filter(lambda x: "router static" in x, core_list))

        if uno_pruebav != "":
            ver = "v_uno"
        if dos_pruebav != "":
            ver = "v_dos"
        
        return version.check_patterns(ver)

    def check_patterns(self, ver):

        if ver == "v_uno":

            patterns = {
                'id': 1,
                'inter': {
                    'p_vpn': ['ip vrf ', 'vrf '],
                    'r_vpn': ['ip vrf forwarding ', 'vrf forwarding '],
                    'p_ipsec': ['secondary'],
                    'r_ipsec': ["ip address", "secondary"],
                    'p_ip': ["ip address "],
                    'r_ip': ['ip address'],
                    'p_descrip': ['description'],
                    'r_descrip': ['description'],
                    'p_vlan': ["encapsulation dot1Q"],
                    'p_policy_in': ["input"],
                    'r_policy_in': ["service-policy input "],
                    'p_policy_out': ["output"],
                    'r_policy_out': ["service-policy output "],
                    'p_status': ['shutdown'],
                    'p_ipv6': ['ipv6']
                },
                'vpn': {
                    'p_vpn': ["ip vrf ", "vrf definition "],
                    'p_rd': ['rd'],
                    'r_rd': ["rd "],
                    'p_rte': ["route-target export"],
                    'r_rte': ["route-target export"],
                    'p_rti': ["route-target import"],
                    'r_rti': ["route-target import"],
                    'p_descrip': ["description"],
                    'r_descrip': ["description "],
                    'p_map': ['map']
                },
                'routes': {
                    'p_routes': ['ip route ']
                },
                'bgp': {
                    'p_vpn': ['vrf ', 'address-family ipv4 vrf '],

                }
            }

        if ver == "v_dos":

            patterns = {
                'id': 2,
                'inter': {
                    'p_vpn': ['vrf', ''],
                    'r_vpn': ['vrf', ''],
                    'p_ipsec': ["secondary"],
                    'r_ipsec': ["ipv4 address", "secondary"],
                    'p_ip': ['ipv4 address'],
                    'r_ip': ['ipv4 address'],
                    'p_descrip': ['description'],
                    'r_descrip': ['description'],
                    'p_vlan': ["encapsulation dot1q"],
                    'p_policy_in': ["input"],
                    'r_policy_in': ["service-policy input "],
                    'p_policy_out': ["output"],
                    'r_policy_out': ["service-policy output "],
                    'p_status': ['shutdown'],
                    'p_ipv6': ['ipv6']
                },
                'vpn': {
                    'p_vpn': ["vrf ", "vrf definition "],
                    'p_rd': ['rd'],
                    'r_rd': ["rd "],
                    'p_rte': ["export route-target"],
                    'r_rte': ["export route-target"],
                    'p_rti': ["import route-target"],
                    'r_rti': ["import route-target"],
                    'p_descrip': ["description"],
                    'r_descrip': ["description "],
                    'p_map': ['map']
                },
                'routes': {
                    'p_routes': ['router static']
                },
                'bgp': {
                    'p_vpn': ['vrf ', 'address-family ipv4 vrf ']
                }
            }

        return patterns

version = Version()