import re
from Get_possible_peers_residential import Get_peers_data

class Get_residential_data:

    def get_data(self, parameters, block_list, ce_cfg, gid_routes, iptv_unicast_routes, version):
        
        package = []
        descrip = "".join(filter(lambda x: 'description ' in x, block_list)).lower()

        """GET DSLAM/GPON NAME THROUGH DESCRIPTION"""
        dslam_name = descrip.split()
        for x in dslam_name:
            if re.findall('-', x) or re.findall('_', x):
                dslam_name = x.upper()
                break

        if re.findall(r'[.]\d+', block_list[0]):
            """FILTER VLAN NUMBER"""
            vlan = ("".join(re.findall(r'[.]\d+', block_list[0])).replace('.', '')).strip()

            """IDENTIFY SPEEDY VLAN"""
            if re.findall('internet', descrip):
                package.append(vlan)
                package.append(dslam_name)
                parameters['VLAN']['TRAFFIC INTERNET'].append(package)

            """IDENTIFY VOIP VLAN"""
            if list(filter(lambda x: 'VOIP-IAD' in x, block_list)) != [] or re.findall('voip', descrip):
                package.append(vlan)
                package.append(dslam_name)
                parameters['VLAN']['TRAFFIC VOIP'].append(package)

            """IDENTIFY MODENS VLAN"""
            if re.findall('modem', descrip):
                package.append(vlan)
                package.append(dslam_name)
                parameters['VLAN']['GESTION MODEMS'].append(package)

            """IDENTIFY ENTERPRISE TRAFFIC VLAN"""
            if re.findall('trafico empresa', descrip):
                package.append(vlan)
                package.append(dslam_name)
                parameters['VLAN']['TRAFFIC ENTERPRISE'].append(package)

            """IDENTIFY GID1 VLAN"""
            if list(filter(lambda x: 'gid1' in x, block_list)) != []:
                routes_list = []
                package.append(vlan)
                package.append(dslam_name)
                #parameters['VLAN']['GESTION GID1'].append(package)

                """GET GID1 STATIC ROUTES"""
                static_routes = list(filter(lambda x: vlan in x, gid_routes))
                for x in static_routes:

                    if version == 1:
                        route = re.findall(r'\d+[.]\d+[.]\d+[.]\d+', x)
                        if len(route) == 3:
                            huawei_route = f'ip route-static vpn-instance gid1 {route[0]} {route[1]} Eth-TrunkETH_NUMBER.TBD {route[2]}'
                            routes_list.append(huawei_route)
                        if len(route) == 2:
                            huawei_route = f'ip route-static vpn-instance gid1 {route[0]} {route[1]} Eth-TrunkETH_NUMBER.TBD {route[0]}'
                            routes_list.append(huawei_route)
                    
                    if version == 2:
                        route = re.findall(r'\d+[.]\d+[.]\d+[.]\d+/\d+', x)
                        if route != []:
                            route = route[0].replace('/', ' ').split()
                            huawei_route = f'ip route-static vpn-instance gid1 {route[0]} {route[1]} Eth-TrunkETH_NUMBER.TBD {route[0]}'
                            routes_list.append(huawei_route)

                    package.append(routes_list)
                parameters['VLAN']['GESTION GID1'].append(package)
                
            """IDENTIFY NGN TRAFFIC VLAN"""
            if re.findall('trafico', descrip) and list(filter(lambda x: 'NGN' in x, block_list)) != []:
                if version == 1:
                    pattern = 'ip address'
                if version == 2:
                    pattern = 'ipv4 address'

                package.append(vlan)
                package.append(dslam_name)
                ipmask = "".join(filter(lambda x: pattern in x, block_list))
                if ipmask != "":
                    ipmask = ipmask.replace(pattern, "").strip()
                    package.append(ipmask)
                parameters['VLAN']['NGN TRAFFIC'].append(package)

            """IDENTIFY NGN SENIALIZATION VLAN"""
            if not re.findall('trafico', descrip) and list(filter(lambda x: 'NGN' in x, block_list)) != []:
                if version == 1:
                    pattern = 'ip address'
                if version == 2:
                    pattern = 'ipv4 address'
                    
                package.append(vlan)
                package.append(dslam_name)
                ipmask = "".join(filter(lambda x: pattern in x, block_list))
                if ipmask != "":
                    ipmask = ipmask.replace(pattern, "").strip()
                    package.append(ipmask)
                parameters['VLAN']['NGN SENIALIZATION'].append(package)

            if list(filter(lambda x: 'IPTV-UNICAST' in x, block_list)) != []:
                peers_obj = Get_peers_data()
                package.append(vlan)
                package.append(dslam_name)

                if version == 1:
                    routes = []
                    ipmask = "".join(filter(lambda x: 'ip address ' in x, block_list))
                    ipmask = ipmask.replace('ip address', "").strip().split(" ")
                    package.append(ipmask)
                    if ipmask != ['']:
                        ip = ipmask[0]
                        mask = ipmask[1]
                        possible_peers = peers_obj.get_data(ip, mask)
                        for x in range(len(possible_peers)):
                            route_ =  list(filter(lambda i: possible_peers[x] in i, iptv_unicast_routes))
                            if route_ != []:
                                for z in route_:
                                    route_filter = re.findall(r'\d+[.]\d+[.]\d+[.]\d+', z)
                                    if len(route_filter) == 3:
                                        huawei_routes = f'ip route-static vpn-instance IPTV-UNICAST {route_filter[0]} {route_filter[1]} {route_filter[2]}'
                                        routes.append(huawei_routes)
                    package.append(routes)

                if version == 2:
                    routes = []
                    ipmask = "".join(filter(lambda x: 'ipv4 address' in x, block_list))
                    ipmask = ipmask.replace('ipv4 address', "").strip().split(" ")
                    package.append(ipmask)
                    if ipmask != ['']:
                        ip = ipmask[0]
                        mask = ipmask[1]
                        possible_peers = peers_obj.get_data(ip, mask)
                        for x in range(len(possible_peers)):
                            route_ =  list(filter(lambda i: possible_peers[x] in i, iptv_unicast_routes))
                            if route_ != []:
                                for z in route_:
                                    z = z.replace('/', ' ').split()
                                    huawei_routes = f'ip route-static vpn-instance IPTV-UNICAST {z[0]} {z[1]} {z[2]}'
                                    routes.append(huawei_routes)
                    package.append(routes)

                parameters['VLAN']['IPTV UNICAST'].append(package)
            
            if list(filter(lambda x: 'IPTV-MULTICAST' in x, block_list)) != []:

                if version == 1:
                    pattern = 'ip address'
                if version == 2:
                    pattern = 'ipv4 address'

                package.append(vlan)
                package.append(dslam_name)
                ipmask = "".join(filter(lambda x: pattern in x, block_list))
                if ipmask != "":
                    ipmask = ipmask.replace(pattern, "").strip()
                    package.append(ipmask)

                parameters['VLAN']['IPTV MULTICAST'].append(package)

            
        else:
            parameters['NAME'] = dslam_name
        




            

        

