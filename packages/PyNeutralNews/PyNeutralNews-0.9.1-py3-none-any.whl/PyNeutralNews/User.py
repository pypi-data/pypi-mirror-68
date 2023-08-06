from .ApiModels import User as Models
from .Connector import Connector


class User(Connector):

    def login(self):
        self.client.login()

    def usage(self):
        return Models.Usage.fill(**locals()).call(self.client)
