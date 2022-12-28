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
                }
            }

        if ver == "v_dos":

            patterns = {
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
                    'p_vpn': ["vrf ", "vrf definition "]
                }
            }

        return patterns

version = Version()