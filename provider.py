# -*- coding: utf-8 -*-
from netatmo_indicator.netatmo_service_wrapper import Netatmo
import requests
import subprocess


class Provider:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def get():
        raise NotImplementedError("Please Implement this method")


class NetatmoProvider(Provider):

    def get(self):
        (data, timestamp) = Netatmo(self.credentials_file).get_data()
        return " ".join(("{}:{}°".format(*i) for i in data.items()))


class WttrInProvider(Provider):

    def get(self):
        r = requests.get("http://wttr.in/Munich?format=\"%C\"")
        return str(r.json())


class TranmissionProvider(Provider):
    def get(self):
        result = ""
        for status in ["Downloading", "Seeding"]:
            bashCommand = "transmission-remote  192.168.0.101:9091 -l | head -n -1 | grep " + \
                status + " | wc -l"

            output, error = subprocess.Popen(
                bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()

            count = int(output)
            if count > 0:
                result = status + ": " + str(count)
        return result


class ProviderFactory:
    def new(self, type_name, credentials_file):
        if type_name == "netatmo":
            return NetatmoProvider(credentials_file)
        if type_name == "wttrin":
            return WttrInProvider("")
        if type_name == "transmission":
            return TranmissionProvider("")
