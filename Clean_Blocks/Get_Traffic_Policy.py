import re

class Get_traffic_policy:

    def get_data_policy_in(self, block_list, parameters):
        
        policy_in = re.findall(r'\d+', "".join(block_list))
        if policy_in != []:
            if not re.findall(r'\d+ mbps', "".join(block_list)):
                first_value = int(int(policy_in[0])) / 1000
            else:
                first_value = int(int(policy_in[0])) * 1000
            policy_in[0] = str(int(first_value))
            parameters['POLICY_IN'] = policy_in

    def get_data_policy_out(self, block_list, parameters):

        sa = "".join(filter(lambda x: "shape" in x, block_list))
        sa = sa.replace("shape average", "").strip().split(" ")
        if sa == ['']:
            sa = "".join(filter(lambda x: "police cir" in x, block_list))
            sa = sa.replace("police cir", "").strip().split(" ")
        if sa[0].isdigit():
            if not re.findall('mbps', "".join(sa)):
                parameters['POLICY_OUT']['shape average'] = str(int(int(sa[0]) / 1000))
            if re.findall('mbps', "".join(sa)):
                parameters['POLICY_OUT']['shape average'] = str(int(int(sa[0]) * 1000))

        sp = "".join(filter(lambda x: "service-policy" in x, block_list)).replace("service-policy ", "").strip()
        parameters['POLICY_OUT']['service-policy'] = sp.replace("service-policy ", "").strip()

    def get_data_flow_queue(self, block_list, parameters):
        
        all_class = [' class MM', ' class ORO',' class PLATA', ' class BRONCE',' class PLATINO',' class VIDEO']

        def get_police_values(class_value):

            for x in block_list:
                first_class = re.findall(class_value, x)
                if first_class != []:
                    parameters['FLOW_QUEUE'][class_value][0] = True
                    first_index = int(block_list.index(first_class[0]))

                    for i in range(first_index, len(block_list)):
                        if re.findall(r'percent \d+', block_list[i]):
                            percent = "".join(re.findall(r'percent \d+', block_list[i]))
                            parameters['FLOW_QUEUE'][class_value][1] = percent.replace('percent', '').strip()
                            break

                        if re.findall(r'bandwidth \d+', block_list[i]):
                            bandwidth = "".join(re.findall(r'bandwidth \d+', block_list[i]))
                            percent = "".join(re.findall(r'\d', bandwidth))
                            rule = int(int(percent)*100 / int(parameters['POLICY_OUT']['shape average']))
                            parameters['FLOW_QUEUE'][class_value][1] = rule
                            break

                        if re.findall(r'police \d+', block_list[i]):
                            bandwidth = "".join(re.findall(r'police \d+', block_list[i]))
                            percent = "".join(re.findall(r'\d', bandwidth))
                            rule = int(int((int(percent)/1000)*100)/ int(parameters['POLICY_OUT']['shape average']))
                            parameters['FLOW_QUEUE'][class_value][1] = rule
                            break

                        if re.findall(r'police rate \d+', block_list[i]):
                            bandwidth = "".join(re.findall(r'police rate \d+', block_list[i]))
                            percent = "".join(re.findall(r'\d', bandwidth))
                            rule = int(int((int(percent)/1000)*100)/ int(parameters['POLICY_OUT']['shape average']))
                            parameters['FLOW_QUEUE'][class_value][1] = rule
                            break

        for x in range(len(all_class)):
            get_police_values(all_class[x])


    
            


        