def open_txt(path):

    configuration_path = path
    text = open(configuration_path, "r")
    text_to_list = list(map(str.rstrip, text))
    text.close()
    return text_to_list