def reset_establish_parameters(parameters):

    for x in parameters['INTER'].keys():
        parameters['INTER'][x] = ""

    for x in parameters['VPN'].keys():
        parameters['VPN'][x] = ""

    parameters['BGP']['STATUS'], parameters['BGP']['PEER'] = False, "" 
    for x in parameters['BGP']['ATTRIBUTES'].keys():
        if x == 'password cipher':
            parameters['BGP']['ATTRIBUTES'][x] = [False, 'XXXX']
        else:
            parameters['BGP']['ATTRIBUTES'][x] = [False, '']

    parameters['RIP']['STATUS'], parameters['RIP']['network'], parameters['RIP']['neighbor'] = False, [], []

    parameters['POLICY_IN'] = []
    parameters['POLICY_OUT']['shape average'], parameters['POLICY_OUT']['service-policy'] = "", ""

    for x in parameters['FLOW_QUEUE'].keys():
        parameters['FLOW_QUEUE'][x] = [False, '']
        
    parameters['ROUTES'] = []
    parameters['OLD_INTERFACE'] = ""

    for x in parameters['ROUTE_MAP_IN'].keys():
        if x == 'route_policy_quantity':
            parameters['ROUTE_MAP_IN'][x] = 0
        else:
            parameters['ROUTE_MAP_IN'][x] = []
        
    for x in parameters['ROUTE_MAP_OUT'].keys():
        if x == 'route_policy_quantity':
            parameters['ROUTE_MAP_OUT'][x] = 0
        else:
            parameters['ROUTE_MAP_OUT'][x] = []
        
    parameters['IP_PREFIX'] = []
    parameters['DISPLAY_COMMAND']['interface'], parameters['DISPLAY_COMMAND']['vlan'] =  'GigabitEthernet', ''

    return parameters

def reset_residential_parameters(residential_parameters):

    residential_parameters['NAME'] = ''
    residential_parameters['VLAN']['TRAFFIC INTERNET'] = []
    residential_parameters['VLAN']['TRAFFIC VOIP'] = []
    residential_parameters['VLAN']['GESTION MODEMS'] = []
    residential_parameters['VLAN']['TRAFFIC ENTERPRISE'] = []
    residential_parameters['VLAN']['GESTION GID1'] = []
    residential_parameters['VLAN']['NGN TRAFFIC'] = []
    residential_parameters['VLAN']['NGN SENIALIZATION'] = []
    residential_parameters['VLAN']['IPTV MULTICAST'] = []
    residential_parameters['VLAN']['IPTV UNICAST'] = []
    residential_parameters['NEW_INTERFACE_1'] = ''
    residential_parameters['NEW_INTERFACE_2'] = ''
    residential_parameters['NEW_ETH'] = 'XX'
    residential_parameters['ID'] = 'XXXXX'

