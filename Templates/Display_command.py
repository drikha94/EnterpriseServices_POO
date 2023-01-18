display_template = [
    f'############ REF:TO_REPLACE\n',
    f'#\n',
    f'display interface brief ',
    f'display arp all | inc ',
    f'ping -vpn-instace VPN_NAME -a IP_MAIN IP_REMOTE\n',
    f'display ip routing-table vpn-instance VPN_NAME\n',
    f'display bgp vpnv4 vpn-instance VPN_NAME routing-table peer IP_REMOTE advertised-routes\n',
    f'display bgp vpnv4 vpn-instance VPN_NAME routing-table peer IP_REMOTE accepted-routes\n',
    f'#\n',
    f'#\n'
]