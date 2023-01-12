from io import open
import re

class Get_bgp_data:

    def get_data(self, block_list, parameters, patterns):

        bgp = parameters['BGP']['ATTRIBUTES']
        ref = parameters['INTER']['REF']
        
        def import_route_static():
            r_e = "".join(filter(lambda x: "redistribute static" in x, block_list))
            bgp['import-route static'][0] = True if r_e != "" else False

        def load_balancing():
            mp = "".join(filter(lambda x: "maximum-paths" in x, block_list)).replace("maximum-paths ", "").strip()
            if mp != "":
                bgp['maximum load'][0] = True
                bgp['maximum load'][1] = mp

        def default_route():
            d_r = "".join(filter(lambda x: "default-information" in x, block_list))
            d_r = "".join(filter(lambda x: "default-originate" in x, block_list)) if d_r == "" else d_r
            bgp['default-route-advertise'][0] = True if d_r != "" else False

        def import_route_rip():
            rip = "".join(filter(lambda x: "redistribute rip" in x, block_list))
            if rip != "":
                bgp['import-route rip'][0] = True 
                bgp['import-route rip'][1] = ref if ref != "" else 'XXXXX'

        def remote_as():
            ra = "".join(filter(lambda x: "remote-as" in x, block_list))
            ra = "".join(re.findall(r'remote-as \d+', ra)).replace('remote-as ', '').strip()
            if ra != "":
                bgp['as-number'][0] = True 
                bgp['as-number'][1] = ra
            
        def description():
            des = "".join(filter(lambda x: "description" in x, block_list))
            des = "".join(re.findall(r'description.+', des)).replace('description ', '').strip()
            bgp['description'][0] = True
            bgp['description'][1] = des if des != "" else parameters['INTER']['DESCRIP']


        def keep_all_routes():
            kar = "".join(filter(lambda x: "soft" in x, block_list))
            bgp['keep-all-routes'][0] = True if kar != "" else False

        def route_limit():
            rl = "".join(filter(lambda x: "maximum-prefix" in x, block_list))
            rl = "".join(re.findall(r'maximum-prefix.+', rl)).replace('maximum-prefix ', '').strip()
            if rl != "":
                bgp['route-limit'][0] = True
                bgp['route-limit'][1] = rl

        def advertise_community():
            ac = "".join(filter(lambda x: "send-community" in x, block_list))
            bgp['advertise-community'][0] = True if ac != "" else False

        def substitute_as():
            sa = "".join(filter(lambda x: "as-override" in x, block_list))
            bgp['substitute-as'][0] = True if sa != "" else False
        
        def password_cipher():
            pc = "".join(filter(lambda x: "password" in x, block_list))
            bgp['password cipher'][0] = True if pc != "" else False

        def ebgp_max_hop():
            emh = "".join(filter(lambda x: "ebgp-multihop " in x, block_list))
            emh = "".join(re.findall(r'ebgp-multihop.+', emh)).replace('ebgp-multihop ', '').strip()
            if emh != "":
                bgp['ebgp-max-hop'][0] = True
                bgp['ebgp-max-hop'][1] = emh

        def allow_as_loop():
            asl = "".join(filter(lambda x: "allowas-in" in x, block_list))
            bgp['allow-as-loop'][0] = True if asl != "" else False
            asl = "".join(re.findall(r'allowas-in.+', asl)).replace('allowas-in ', '').strip()
            bgp['allow-as-loop'][1] = asl if asl != "" else ""
        
        def reflect_client():
            rrc = "".join(filter(lambda x: "route-reflector-client" in x, block_list))
            bgp['reflect-client'][0] = True if rrc != "" else False
            
        def route_update_interval():
            ai = "".join(filter(lambda x: "advertisement-interval" in x, block_list))
            ai = "".join(re.findall(r'advertisement-interval.+', ai)).replace('advertisement-interval ', '').strip()
            if ai != "":
                bgp['route-update'][0] = True
                bgp['route-update'][1] = ai

        def route_map(traffic, key, to_replace_one, to_replace_two):
            if patterns['id'] == 1:
                for x in block_list:
                    if re.findall(r'route-map.+ '+traffic, x):
                        rm = re.findall(r'route-map.+ '+traffic, x)
                        bgp[key][0] = True
                        bgp[key][1] = "".join(rm).replace(to_replace_one, '').replace(to_replace_two, '').strip()


        def rd_version_two():
            if patterns['id'] == 2:
                parameters['VPN']['RD'] = "".join(re.findall(r'rd \d+:\d+', "".join(block_list)))
                parameters['VPN']['RD'] = parameters['VPN']['RD'].replace("rd ", "").strip()

        import_route_static(), load_balancing(), default_route(), import_route_rip(), remote_as(), description()
        keep_all_routes(), route_limit(), advertise_community(), substitute_as(), password_cipher(), ebgp_max_hop()
        allow_as_loop(), reflect_client(), route_update_interval(), route_map('in', 'route-policy_in', 'route-map ', ' in')
        route_map('out', 'route-policy_out', 'route-map ', ' out'), rd_version_two()



                
        


        


            




                    
                

        
        



                



            


