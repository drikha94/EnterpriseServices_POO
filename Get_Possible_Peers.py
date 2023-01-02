class Get_peers_data:

    def __init__(self):

        self.bucle = 2
        self.possible_peers = []
        self.sum_peer = [1, -1, 5, -5]

    def get_data(self, parameters):

        ip_div = parameters['INTER']['IP'].split(".")
        ip_div = [int(x) for x in ip_div]

        if parameters['INTER']['MASK'] == "255.255.255.248":
            self.bucle = 4

        for peer in range(self.bucle):
            peers = "{}.{}.{}.{}".format(ip_div[0], ip_div[1], ip_div[2], (ip_div[3] + self.sum_peer[peer]))
            self.possible_peers.append(peers)
        
        return self.possible_peers