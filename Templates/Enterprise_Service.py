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

bgp_template = [
    f'bgp 22927\n', 
    f' ipv4-family vpn-instance VPN_NAME\n',
    f' import-route direct\n',
    f' import-route static\n',
    f' import-route rip RIP_NUMBER\n',
    f' maximum load-balancing ibgp BALANCING_NUMBER\n',
    f' peer IP_PEER as-number AS_NUMBER\n',
    f' peer IP_PEER description BGP_DESCRIPTION\n',
    f' peer IP_PEER advertise-community\n',
    f' peer IP_PEER keep-all-routes\n',
    f' peer IP_PEER substitute-as\n',
    f' peer IP_PEER fake-as 10834\n',
    f' peer IP_PEER route-limit ROUTE_LIMIT\n',
    f' peer IP_PEER default-route-advertise\n',
    f' peer IP_PEER password cipher PASSWORD_CIPHER\n',
    f' peer IP_PEER ebgp-max-hop MAX_HOP_NUMBER\n',
    f' peer IP_PEER allowas-in ALLOW_IN_NUMBER\n',
    f' peer IP_PEER route-update-interval ROUTE_INTERVAL_NUMBER\n',
    f' peer IP_PEER reflect-client\n',
    f' peer IP_PEER enable\n'
]

