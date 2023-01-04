import re

class Select_peer:

    def peer_filter(self, peers, block_list_string):

        if peers != []:
            peer = peers[0] if re.findall(f'{peers[0]} ', block_list_string) and peers[0] != "" else ""
            peer = peers[1] if re.findall(f'{peers[1]} ', block_list_string) and peers[1] != "" and peer == "" else peer

            if len(peers) == 4 and peer == "":
                peer = peers[2] if re.findall(f'{peers[2]} ', block_list_string) and peers[2] != "" and peer == "" else peer
                peer = peers[3] if re.findall(f'{peers[3]} ', block_list_string) and peers[3] != "" and peer == "" else peer

            return peer