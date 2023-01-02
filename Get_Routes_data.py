import re

class Get_routes_data:

    def __init__(self):

        self.routes = []

    def get_data(self, parameters, block_list, peers, patterns):

        filter_routes = []

        if block_list[0] != []:
            num = 0
        if block_list[1] != []:
            num = 1

        for i in range(len(peers)):
            filter_routes.append(list(filter(lambda x: peers[i] in x, block_list[num])))

        print(filter_routes)
        for x in filter_routes:
            if patterns['id'] == 1 and x != "":
                pass  

            if patterns['id'] == 2 and x != "":
                if re.findall('description', x):
                    x = "".join(re.findall(r'.+description', x))
                    x = x.replace('description', '').replace('/', ' ').strip()
                    self.routes.append(x)

            

        
        #print(self.routes)

        