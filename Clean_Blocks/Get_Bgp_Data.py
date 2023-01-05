from io import open
import re

class Get_bgp_data:

    def get_data(self, block_list, parameters, patterns):
        
        def import_route_static():
            r_e = "".join(filter(lambda x: "redistribute static" in x, block_list))
            if r_e != "":
                parameters['BGP']['ATTRIBUTES']['import-route static'][0] = True

        def load_balancing():
            mp = "".join(filter(lambda x: "maximum-paths" in x, block_list)).replace("maximum-paths ", "").strip()
            if mp != "":
                parameters['BGP']['ATTRIBUTES']['maximum load-balancing ibgp'][0] = True
                parameters['BGP']['ATTRIBUTES']['maximum load-balancing ibgp'][1] = mp

        def default_route():
            d_r = "".join(filter(lambda x: "default-information" in x, block_list))
            if d_r != "":
                parameters['BGP']['ATTRIBUTES']['default-route-advertise'][0] = True

        def import_route_rip():
            rip = "".join(filter(lambda x: "redistribute rip" in x, block_list))
            if rip != "":
                parameters['BGP']['ATTRIBUTES']['import-route rip'][0] = True 
                parameters['BGP']['ATTRIBUTES']['import-route rip'][1] = parameters['INTER']['REF']

        def remote_as():
            ra = "".join(filter(lambda x: "remote-as" in x, block_list))
            ra = "".join(re.findall(r'remote-as \d+', ra)).replace('remote-as ', '').strip()
            if ra != "":
                parameters['BGP']['ATTRIBUTES']['as-number'][0] = True 
                parameters['BGP']['ATTRIBUTES']['as-number'][1] = ra
            
        def description():
            des = "".join(filter(lambda x: "description" in x, block_list))
            des = "".join(re.findall(r'description.+', des)).replace('description ', '').strip()
            if des != "":
                parameters['BGP']['ATTRIBUTES']['description'][0] = True
                parameters['BGP']['ATTRIBUTES']['description'][1] = des

        def keep_all_routes():
            kar = "".join(filter(lambda x: "soft" in x, block_list))
            if kar != "":
                parameters['BGP']['ATTRIBUTES']['keep-all-routes'][0] = True

        def route_limit():
            rl = "".join(filter(lambda x: "maximum-prefix" in x, block_list))
            rl = "".join(re.findall(r'maximum-prefix.+', rl)).replace('maximum-prefix ', '').strip()
            if rl != "":
                parameters['BGP']['ATTRIBUTES']['route-limit'][0] = True
                parameters['BGP']['ATTRIBUTES']['route-limit'][1] = rl

        def advertise_community():
            ac = "".join(filter(lambda x: "send-community" in x, block_list))
            if ac != "":
                parameters['BGP']['ATTRIBUTES']['advertise-community'][0] = True

        def substitute_as():
            sa = "".join(filter(lambda x: "as-override" in x, block_list))
            if sa != "":
                parameters['BGP']['ATTRIBUTES']['substitute-as'][0] = True
        
        def password_cipher():
            pc = "".join(filter(lambda x: "password" in x, block_list))
            if pc != "":
                parameters['BGP']['ATTRIBUTES']['password cipher'][0] = True

        def ebgp_max_hop():
            emh = "".join(filter(lambda x: "ebgp-multihop " in x, block_list))
            emh = "".join(re.findall(r'ebgp-multihop.+', emh)).replace('ebgp-multihop ', '').strip()
            if emh != "":
                parameters['BGP']['ATTRIBUTES']['ebgp-max-hop'][0] = True
                parameters['BGP']['ATTRIBUTES']['ebgp-max-hop'][1] = emh

        def allow_as_loop():
            asl = "".join(filter(lambda x: "allowas-in" in x, block_list))
            if asl != "":
                parameters['BGP']['ATTRIBUTES']['allow-as-loop'][0] = True
            asl = "".join(re.findall(r'allowas-in.+', asl)).replace('allowas-in ', '').strip()
            if asl != "":
                parameters['BGP']['ATTRIBUTES']['allow-as-loop'][1] = asl
        
        def reflect_client():
            rrc = "".join(filter(lambda x: "route-reflector-client" in x, block_list))
            if rrc != "":
                parameters['BGP']['ATTRIBUTES']['reflect-client'][0] = True
            
        def route_update_interval():
            ai = "".join(filter(lambda x: "advertisement-interval" in x, block_list))
            ai = "".join(re.findall(r'advertisement-interval.+', ai)).replace('advertisement-interval ', '').strip()
            if ai != "":
                parameters['BGP']['ATTRIBUTES']['route-update-interval'][0] = True
                parameters['BGP']['ATTRIBUTES']['route-update-interval'][1] = ai

        def rd_version_two():
            if patterns['id'] == 2:
                parameters['VPN']['RD'] = "".join(re.findall(r'rd \d+:\d+', "".join(block_list)))
                parameters['VPN']['RD'] = parameters['VPN']['RD'].replace("rd ", "").strip()

        import_route_static(), load_balancing(), default_route(), import_route_rip(), remote_as(), description()
        keep_all_routes(), route_limit(), advertise_community(), substitute_as(), password_cipher(), ebgp_max_hop()
        allow_as_loop(), reflect_client(), route_update_interval(), rd_version_two()


                
        


        


            




                    
                

        
        



                



            


