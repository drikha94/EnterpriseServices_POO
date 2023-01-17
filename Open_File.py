def open_txt(path):

    configuration_path = path
    text = open(configuration_path, "r")
    text_to_list = list(map(str.rstrip, text))
    text.close()
    return text_to_list

def append_txt(path):

    script_path = path
    text = open(script_path, "a")
    #text.close()
    return text