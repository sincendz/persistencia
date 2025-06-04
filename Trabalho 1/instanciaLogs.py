import yaml, logging
class Logs:
    
    def __init__(self):    
        with open('config.yaml' , 'r') as file: # r -> read
            config = yaml.safe_load(file)
        self.setup_logging(config['logging'])
       

    def setup_logging(self,config):
        logging.basicConfig(
            level = config['level'],
            format = config['format'],
            filename= config['file'],
            filemode='a',
        )



