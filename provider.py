# -*- coding: utf-8 -*-
from netatmo_indicator.netatmo_service_wrapper import Netatmo


class Provider:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def get():
        raise NotImplementedError("Please Implement this method")


class NetatmoProvider(Provider):

    def get(self):
        (data, timestamp) = Netatmo(self.credentials_file).get_data()
        return " ".join(("{}:{}°".format(*i) for i in data.items()))


class ProviderFactory:
    def new(self, type_name, credentials_file):
        if type_name == "netatmo":
            return NetatmoProvider(credentials_file)
