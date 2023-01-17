import re

class Get_map_data:

    def get_data(self, block_list, parameters, patterns, core_list, map):
        
        def rule():
            
            rule = [False, '']
            permit = "".join(re.findall(r'permit \d+', block_list[0])).replace('permit ', '').strip()
            deny = "".join(re.findall(r'deny \d+', block_list[0])).replace('deny ', '').strip()
            if permit != "":
                rule[0] = True
                rule[1] = permit
            if deny != "":
                rule[0] = False
                rule[1] = deny
            parameters[map]['rule'].append(rule)

        def set_local_preference():
            local = [False, '']
            set_local = "".join((filter(lambda x: "set local-preference" in x, block_list))).replace('set local-preference', '').strip()
            if set_local != "":
                local[0] = True
                local[1] = set_local
            parameters[map]['set local-preference'].append(local)

        def match_interface():
            match_int = [False, '']
            match_inter = "".join((filter(lambda x: "match interface" in x, block_list))).replace('match', '').strip()
            if match_inter != "":
                match_int[0] = True
                match_int[1] = match_inter
            parameters[map]['match interface'].append(match_int)
        
        def match_ip():
            match_ip_list = [False, '']
            match_ip = "".join((filter(lambda x: "match ip address prefix-list" in x, block_list)))
            match_ip = match_ip.replace('match ip address prefix-list', '').strip() if match_ip != "" else ""
            if match_ip != "":
                match_ip_list[0] = True
                match_ip_list[1] = match_ip
            parameters[map]['match ip address prefix-list'].append(match_ip_list)

        def match_ipv6():
            match_6 = [False, '', []]
            match_ipv6 = "".join((filter(lambda x: "match ipv6 address prefix-list" in x, block_list)))
            if match_ipv6 != "":
                match_ipv6 = match_ipv6.replace('match ipv6 address prefix-list', '').strip()
                match_6[0] = True
                match_6[1] = match_ipv6
            parameters[map]['match ipv6 address prefix-list'].append(match_6)
                        
        def set_as_path():
            set_list = [False, '']
            set_as = "".join((filter(lambda x: "set as-path prepend" in x, block_list)))
            if set_as != "":
                set_as = set_as.replace('set as-path prepend', '').strip()
                set_list[0] = True
                set_list[1] = set_as
            parameters[map]['set as-path prepend'].append(set_list)

        def set_extcommunity():
            set_ext_list = [False, '']
            set_ext = "".join((filter(lambda x: "set extcommunity rt" in x, block_list)))
            if set_ext != "":
                set_ext =  re.findall(r'\d+[:]\d+', set_ext)
                set_ext_list[0] = True
                set_ext_list[1] = set_ext
            parameters[map]['set extcommunity'].append(set_ext_list)
        
        def match_tag():
            tag_list = [False, '']
            tag = "".join((filter(lambda x: "match tag" in x, block_list)))
            if tag != "":
                tag = tag.replace('match tag', '').strip()
                tag_list[0] = True
                tag_list[1] = tag
            parameters[map]['match tag'].append(tag_list)

        rule(), set_local_preference(), match_interface(), match_ip(), match_ipv6(), set_as_path(), set_extcommunity(), match_tag()