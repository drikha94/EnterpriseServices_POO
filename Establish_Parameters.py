parameters = {
    'INTER': {
        'VPN': '', 
        'IP_SEC': '', 
        'MASK_SEC': '', 
        'IP': '', 
        'MASK': '',
        'DESCRIP': '',
        'VLAN_ONE': '',
        'VLAN_TWO': '',
        'POLICY_IN': '',
        'POLICY_OUT': '',
        'STATUS': '',
        'IPV6': '',
        'REF': ''
    },
    'VPN': {
        'RD': '',
        'RTE': '',
        'RTI': '',
        'DESCRIP': '',
        'MAP': ''
    },
    'BGP': {
        'PEER': '',
        'ATTRIBUTES': {
            'bgp 22927': [True, ''],
            'ipv4-family vpn-instance': [True, ''],
            'import-route direct': [True, ''],
            'import-route static': [False, 'N/A'],
            'import-route rip': [False, ''],
            'maximum load-balancing ibgp': [False, ''],
            'as-number': [False, ''],
            'description': [False, ''],
            'advertise-community': [False, 'N/A'],
            'keep-all-routes': [False, ''],
            'substitute-as': [False, 'N/A'],
            'fake-as': [True, ''],
            'route-limit': [False, ''],
            'default-route-advertise': [False, 'N/A'],
            'password cipher': [False, ''],
            'ebgp-max-hop': [False, ''],
            'allow-as-loop': [False, ''],
            'route-update-interval': [False, ''],
            'reflect-client': [False, 'N/A'],
            'enable': [True, 'N/A']
            
        }
    },
    'POLICY_IN': [],
    'POLICY_OUT': {
        'shape average': '',
        'service-policy': ''
    },
    'FLOW_QUEUE':{
        ' class MM': [False, ''],
        ' class ORO': [False, ''],
        ' class PLATA': [False, ''],
        ' class BRONCE': [False, ''],
        ' class PLATINO':[False, ''],
        ' class VIDEO':[False, '']
    },
    'ROUTES': []
}