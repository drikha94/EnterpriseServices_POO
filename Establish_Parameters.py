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
        'STATUS': False,
        'PEER': '',
        'ATTRIBUTES': {
            'import-route static': [False, 'N/A'],
            'import-route rip': [False, ''],
            'maximum load': [False, ''],
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
            'route-update': [False, ''],
            'reflect-client': [False, 'N/A'],
            'route-policy_in': [False, ''],
            'route-policy_out': [False, '']
        }
    },
    'RIP': {
        'STATUS': False,
        'network': [],
        'neighbor': []
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
    'ROUTES': [],
    'NEW_INTERFACE': '55',
    'OLD_INTERFACE': '',
    'ROUTE_MAP_IN':{
        'rule': [],                                   #EL TRUE HACER REFERENCIA AL PERMIT, EL FALSE AL DENY, LAS COMILLAS AL NMR
        'set local-preference': [],
        'match interface': [],
        'match ip address prefix-list': [],
        'match ipv6 address prefix-list': [],     #SET ALARM
        'set as-path prepend': [],                    #SET ALARM
        'set extcommunity': [],
        'match tag': []                               #SET ALARM
    },
    'ROUTE_MAP_OUT':{
        'rule': [],                                   #EL TRUE HACER REFERENCIA AL PERMIT, EL FALSE AL DENY, LAS COMILLAS AL NMR
        'set local-preference': [],
        'match interface': [],
        'match ip address prefix-list': [],                               
        'match ipv6 address prefix-list': [],
        'set as-path prepend': [],
        'set extcommunity': [],
        'match tag': [],
        'match ip address' : []
    }
}