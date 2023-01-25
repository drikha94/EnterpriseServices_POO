from io import open
#from itertools import *
import re

class Get_Interface_Data:

    def get_data(self, parameters, block_list, patterns):
        """EXTRAE LOS PARAMETROS QUE CONTIENE EL BLOQUE DE LA INTERFAZ Y ES ALMACENADO EN EL DICCIONARIO parameters"""

        def get_vpn():

            """SE BUSCA EL NOMBRE DE LA VPN DENTRO DEL BLOQUE QUE CONTIENE LOS PARAMETROS DE LA INTERFAZ"""
            parameters['INTER']['VPN'] = "".join(filter(lambda x: patterns['inter']['p_vpn'][0] in x, block_list))
            parameters['INTER']['VPN'] = parameters['INTER']['VPN'].replace(patterns['inter']['r_vpn'][0], "").strip()
            if parameters['INTER']['VPN'] == "":
                parameters['INTER']['VPN'] = "".join(filter(lambda x: patterns['inter']['p_vpn'][1] in x, block_list))
                parameters['INTER']['VPN'] = parameters['INTER']['VPN'].replace(patterns['inter']['r_vpn'][1], "").strip()

        def get_ipsec():

            """BUSCA LA IP SEC, LA SEPARA DE LA MASK Y LA ALMACENA EN EL DICCIONARIO, Y LA ELIMINA DEL BLOQUE"""
            secondary = "".join(filter(lambda x: patterns['inter']['p_ipsec'][0] in x, block_list))
            if secondary != "":
                secondary_bkp = secondary
                secondary = secondary.replace(patterns['inter']['r_ipsec'][0], "")
                secondary = secondary.replace(patterns['inter']['r_ipsec'][1], "").strip().split(" ")
                block_list.remove(secondary_bkp)
                parameters['INTER']['IP_SEC'] = secondary[0]
                parameters['INTER']['MASK_SEC'] =  secondary[1]

        def get_ip():

            """BUSCA LA IP PRINCIPAL DEL SERVICIO, LA SEPARA DE LA MASCARA Y LA ALMACENA EN EL DICCIONARIO"""
            ipmask = "".join(filter(lambda x: patterns['inter']['p_ip'][0] in x, block_list))
            ipmask = ipmask.replace(patterns['inter']['r_ip'][0], "").strip().split(" ")
            if ipmask != ['']:
                parameters['INTER']['IP'] = ipmask[0]
                parameters['INTER']['MASK'] = ipmask[1]

        def get_description():

            """BUSCA LA DESCRIPCION DE LA INTERFACE Y LA ALMACENA EN EL DICCIONARIO"""
            description = "".join(filter(lambda x: patterns['inter']['p_descrip'][0] in x, block_list))
            parameters['INTER']['DESCRIP'] = description.replace(patterns['inter']['r_descrip'][0], "").strip()
            parameters['INTER']['DESCRIP'] = 'XXXXX' if parameters['INTER']['DESCRIP'] == '' else parameters['INTER']['DESCRIP']

        def get_vlans():

            """BUSCA LAS VLAN (PRINCIPAL Y SECUNDARIA) Y LAS ALMACENA EN EL DICCIONARIO"""
            vlan = "".join(filter(lambda x: patterns['inter']['p_vlan'][0] in x, block_list)).strip().split(" ")
            if len(vlan) == 3:
                parameters['INTER']['VLAN_ONE'] = "".join(vlan[2]).strip()
            if len(vlan) == 5:
                parameters['INTER']['VLAN_ONE'] = "".join(vlan[2]).strip()
                parameters['INTER']['VLAN_TWO'] = "".join(vlan[4]).strip()

            """ACA SE DEFINE LA VLAN EN FUNCION DEL TIPO DE CABLEADO, PARA SER USADO POSTERIORMENTE EN LOS TEMPLATE DE GESTION"""
            if parameters['CABLING_TYPE'] == 'ELECTRIC':
                if parameters['INTER']['VLAN_ONE'] != "" and parameters['INTER']['VLAN_TWO'] != "":
                    parameters['DISPLAY_COMMAND']['vlan'] = parameters['INTER']['VLAN_TWO']
                if parameters['INTER']['VLAN_ONE'] != "" and parameters['INTER']['VLAN_TWO'] == "":
                    parameters['DISPLAY_COMMAND']['vlan'] = ""
            if parameters['CABLING_TYPE'] == 'FIBER':
                if parameters['INTER']['VLAN_ONE'] != "" and parameters['INTER']['VLAN_TWO'] != "":
                    parameters['DISPLAY_COMMAND']['vlan'] = parameters['INTER']['VLAN_ONE'] + parameters['INTER']['VLAN_TWO']
                if parameters['INTER']['VLAN_ONE'] != "" and parameters['INTER']['VLAN_TWO'] == "":
                    parameters['DISPLAY_COMMAND']['vlan'] = parameters['INTER']['VLAN_ONE']
            if not re.findall('/', parameters['NEW_INTERFACE']):
                parameters['DISPLAY_COMMAND']['interface'] = 'Eth-Trunk'

        def get_policy():

            """BUSCA EL SERVICICE POLICY IN Y OUT Y LO ALMACENA EN EL DICCIONARIO"""
            policy_in = "".join(filter(lambda x: patterns['inter']['p_policy_in'][0] in x, block_list))
            parameters['INTER']['POLICY_IN'] = policy_in.replace(patterns['inter']['r_policy_in'][0], "").strip()
            policy_out = "".join(filter(lambda x: patterns['inter']['p_policy_out'][0] in x, block_list))
            parameters['INTER']['POLICY_OUT'] = policy_out.replace(patterns['inter']['r_policy_out'][0], "").strip()

        def get_status():

            """SE VERIFICA EL ESTADO DE LA INTERFAZ (ENCENDIDA O APAGADA) Y SE ALMACENA EN EL DICCIONARIO"""
            status = "".join(filter(lambda x: patterns['inter']['p_status'][0] in x, block_list)).strip()
            if status == "shutdown":
                parameters['INTER']['STATUS'] = status

        def get_ivp6():

            """VERIFICA SI HAY IPV6 EN EL BLOQUE"""
            parameters['INTER']['IPV6'] = "".join(filter(lambda x: patterns['inter']['p_ipv6'][0] in x, block_list))

        def get_ref():

            """FILTRA LA DESCRIPCION PARA UBICAR UNICAMENTE EL NUMERO DE LA REFERENCIA"""
            ref = "".join(re.findall(r'REF...\d+', parameters['INTER']['DESCRIP']))
            parameters['INTER']['REF'] = "".join(re.findall(r'\d', ref))

        get_vpn(), get_ipsec(), get_ip(), get_description(), get_vlans(), get_policy(), get_status(), get_ivp6(), get_ref()

        return parameters