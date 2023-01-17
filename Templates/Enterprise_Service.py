policy_template = [
    f'traffic classifier default\n',
    f' if-match any\n',
    f' commit\n',
    f' quit\n',
    f'#\n',
    f'traffic behavior ENLACE_XX\n',
    f' car cir number_one cbs number_two pbs number_tree green pass red discard\n',
    f'#\n', 
    f' traffic policy ENLACE_XX\n',
    f' undo share-mode\n', 
    f' statistics enable\n', 
    f' classifier default behavior ENLACE_XX\n',
    f'#\n',
    f'#'
]
prefix_template = [
    f'ip ip-prefix PREFIX_NAME index INDEX_NUMBER RULE_NAME IP_MASK\n',   #less-equal 25
    f'#\n'
]

policy_map_template = [
    f'route-policy NAME_POLICY NAME_RULE node NUMBER_RULE\n',
    f' apply local-preference TO_REPLACE\n',
    f' if-match ip-prefix TO_REPLACE\n',
    f' if-match ip-prefix TO_REPLACE\n',
    f' if-match as-path-filter TO_REPLACE\n',
    f' apply as-path TO_REPLACE additive\n',
    f' if-match community-filter TO_REPLACE\n',
    f' apply extcommunityTO_REPLACE',
    f' if-match tag TO_REPLACE\n',
    f'#\n'
]

vpn_template = [
    f'ip vpn-instance VPN_NAME\n',
    f' description ### VPN_DESCRIPTION ###\n',
    f' ipv4-family\n',
    f'  route-distinguisher ROUTE_DISTINGUISHER\n',
    f'  vpn-target RTE_NUMBER export-extcommunity\n',
    f'  vpn-target RTI_NUMBER import-extcommunity\n',
    f'  apply-label per-instance\n',
    f'#\n',
    f'#\n'
]

rip_template = [
    f'rip RIP_NUMBER vpn-instance VPN_NAME\n',
    f' import-route bgp cost 1\n',
    f' network PEER_IP\n',
    f' peer PEER_IP\n',
    f' version 2\n',
    f' undo summary\n',
    f'#'
]

bgp_template = [
    f'bgp 22927\n', 
    f' ipv4-family vpn-instance VPN_NAME\n',
    f' import-route direct\n',
    f' import-route static\n',
    f' import-route rip TO_REPLACE\n',
    f' maximum load-balancing ibgp TO_REPLACE\n',
    f' peer IP_PEER as-number TO_REPLACE\n',
    f' peer IP_PEER description TO_REPLACE\n',
    f' peer IP_PEER advertise-community\n',
    f' peer IP_PEER keep-all-routes\n',
    f' peer IP_PEER substitute-as\n',
    f' peer IP_PEER fake-as 10834\n',
    f' peer IP_PEER route-limit TO_REPLACE\n',
    f' peer IP_PEER default-route-advertise\n',
    f' peer IP_PEER password cipher TO_REPLACE\n',
    f' peer IP_PEER ebgp-max-hop TO_REPLACE\n',
    f' peer IP_PEER allowas-in TO_REPLACE\n',
    f' peer IP_PEER route-update-interval TO_REPLACE\n',
    f' peer IP_PEER reflect-client\n',
    f' pree IP_PEER route-policy TO_REPLACE import\n',
    f' pree IP_PEER route-policy TO_REPLACE export\n',
    f' peer IP_PEER enable\n',
    f'#\n'
]

flow_template = [
    f'flow-queue SERVICE_POLICY\n',  
    f'  queue ef pq shaping shaping-percentage PERCENT_NUMBER\n',
    f'  queue AF1 wfq weight PERCENT_NUMBER\n',
    f'  queue AF2 wfq weight PERCENT_NUMBER\n',
    f'  queue AF3 wfq weight PERCENT_NUMBER\n',
    f'  queue AF4 wfq weight PERCENT_NUMBER\n',
    f'  queue BE wfq weight PERCENT_NUMBER\n',
    f'  quit\n',
    f'commit\n',
    f'#\n',
    f'qos-profile QOS_PROFILE\n',
    f' user-queue cir SHAPE_AVERAGE flow-queue SERVICE_POLICY\n',
    f'#\n',
    f'#\n'
]

interface_template = [ 
    'interface GigabitEthernetX/X/X.VLANC\n',
    ' shutdown\n',
    ' Vlan-type dot1q VLANUNO\n',
    ' encapsulation qinq-termination\n',
    ' qinq termination pe-vid VLANUNO ce-vid VLANDOS\n',
    ' ip binding vpn-instance VPN_NAME\n',
    ' description NAME_SERVICE\n',
    ' ip address NAME_SERVICE\n',
    ' ip address NAME_SERVICE sub\n',
    ' traffic-policy NAME_SERVICE inbound\n',
    ' traffic-policy NAME_SERVICE outbound\n',
    ' qos-profile NAME_SERVICE outbound\n',
    ' statistic enable\n',
    ' trust upstream default\n',
    ' arp broadcast enable\n',
    'commit\n',
    '#\n',
    '#'
]

routes_template = [
    'ip route-static vpn-instance VPN_NAME IPFINAL_MASK_IPPEER description *** VPN_NAME REF:REF_NAME ***\n'
]
