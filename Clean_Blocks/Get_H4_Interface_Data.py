import re

class Get_h4_interface_data:

    def get_data(self, parameters, block_list):

        get_rx_power =  "".join(filter(lambda x: 'Rx Power:' in x, block_list))
        get_rx_power = re.findall(r'.\d+[.]\d+[d][B][m]', get_rx_power)
        parameters['H4_PORT_STATE']['RX_POWER'] = "".join(get_rx_power)
        
        get_tx_power = "".join(filter(lambda x: 'Tx Power:' in x, block_list))
        get_tx_power = re.findall(r'.\d+[.]\d+[d][B][m]', get_tx_power)
        parameters['H4_PORT_STATE']['TX_POWER'] = "".join(get_tx_power)

        bw =  "".join(filter(lambda x: 'Port BW:' in x, block_list)).split(',')
        if bw != [""]:
            parameters['H4_PORT_STATE']['BW'] = bw[0].replace('Port BW:', '').strip()
            parameters['H4_PORT_STATE']['SFP'] =  bw[1].replace('Transceiver max BW:', '').strip()
            parameters['H4_PORT_STATE']['CABLING'] = 'Fiber' if re.findall('SingleMode', bw[2]) else 'Electric'
        
        traffic_in = "".join(filter(lambda x: 'Last 30 seconds input utility rate:' in x, block_list))
        parameters['H4_PORT_STATE']['TRAFFIC_IN'] = traffic_in.replace('Last 30 seconds input utility rate:', '').strip()
        

        traffic_out = "".join(filter(lambda x: 'Last 30 seconds output utility rate:' in x, block_list))
        parameters['H4_PORT_STATE']['TRAFFIC_OUT'] = traffic_out.replace('Last 30 seconds output utility rate:', '').strip()

        state = block_list[0]
        parameters['H4_PORT_STATE']['STATE'] = 'UP' if re.findall('UP', state) else 'DOWN'





