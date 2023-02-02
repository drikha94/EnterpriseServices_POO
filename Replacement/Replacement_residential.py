class Service_template_res:

    def __init__(self, residential_parameters, path_script):

        self.residential_parameters = residential_parameters
        self.path_script = path_script
        self.add_script = open(self.path_script, "a")

    def write_template(self, template):

        self.add_script.write("".join(template))
