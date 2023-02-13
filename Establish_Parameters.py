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
            'import-route static': [False, ''],
            'import-route rip': [False, ''],
            'maximum load': [False, ''],
            'as-number': [False, ''],
            'description': [False, ''],
            'advertise-community': [False, ''],
            'keep-all-routes': [False, ''],
            'substitute-as': [False, ''],
            'fake-as': [True, ''],
            'route-limit': [False, ''],
            'default-route-advertise': [False, ''],
            'password cipher': [False, 'XXXX'],
            'ebgp-max-hop': [False, ''],
            'allow-as-loop': [False, ''],
            'route-update': [False, ''],
            'reflect-client': [False, ''],
            'route-policy_in': [False, ''],
            'route-policy_out': [False, ''],
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
    'NEW_INTERFACE': 'X/X/X',
    'OLD_INTERFACE': '',
    'ROUTE_MAP_IN':{
        'route_policy_quantity': 0,
        'rule': [],                                   #EL TRUE HACER REFERENCIA AL PERMIT, EL FALSE AL DENY, LAS COMILLAS AL NMR
        'set local-preference': [],
        'match interface': [],                        #SET ALARM
        'match ip address prefix-list': [],
        'match ipv6 address prefix-list': [],         #SET ALARM
        'set as-path prepend': [],                    
        'set extcommunity': [],
        'match tag': []                               
    },
    'ROUTE_MAP_OUT':{
        'route_policy_quantity': 0,
        'rule': [],                                   #EL TRUE HACER REFERENCIA AL PERMIT, EL FALSE AL DENY, LAS COMILLAS AL NMR
        'set local-preference': [],
        'match interface': [],
        'match ip address prefix-list': [],                               
        'match ipv6 address prefix-list': [],
        'set as-path prepend': [],
        'set extcommunity': [],
        'match tag': [],
        'match ip address' : []
    },
    'IP_PREFIX': [],
    'DISPLAY_COMMAND':{
        'interface': 'GigabitEthernet',
        'vlan': ''
    },
    'MANAGEMENT_DATA':{
        'mgmt_ip': 'X.X.X.X',
        'device_name': 'DEVICE_NAME',
        'ID': 'ID_NUMBER',
        'ADRED': 'ADRED_NUMBER',
        'RAZON_SOCIAL': 'RAZON_SOCIAL',
        'T5_REMOTE_PORT': 'REMOTE_PORT'
    },
    'CABLING_TYPE':'FIBER',
    'H4_PORT_STATE':{
        'RX_POWER': '-',
        'TX_POWER': '-',
        'BW': '-',
        'SFP': '-',
        'CABLING': '-',
        'TRAFFIC_IN': '-',
        'TRAFFIC_OUT': '-',
        'STATE': '-'
    },
    'H4_NAME': ''
}

residential_parameters = {
    'NAME': '',
    'VLAN': {
        'TRAFFIC INTERNET': [],
        'TRAFFIC VOIP': [],
        'GESTION MODEMS': [],
        'TRAFFIC ENTERPRISE': [],
        'GESTION GID1': [],
        'NGN TRAFFIC': [],
        'NGN SENIALIZATION': [],
        'IPTV MULTICAST': [],
        'IPTV UNICAST': []
    },
    'NEW_INTERFACE_1': '',
    'NEW_INTERFACE_2': '',
    'NEW_ETH': 'XX',
    'ID': 'XXXXX'
}