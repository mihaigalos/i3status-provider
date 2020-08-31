# -*- coding: utf-8 -*-
from netatmo_indicator.netatmo_service_wrapper import Netatmo
import requests
import subprocess


class Provider:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def get():
        raise NotImplementedError("Please Implement this method")

    def isJson(self, input):
        try:
            json_object = json.loads(input)
        except ValueError as e:
            return False
        return True


class NetatmoProvider(Provider):
    def get(self):
        (data, timestamp) = Netatmo(self.credentials_file).get_data()
        return " ".join(("{}:{}°".format(*i) for i in data.items()))


class WttrInProvider(Provider):
    def get(self):
        response = requests.get('http://wttr.in/Munich?format="%C"')
        try:
            result = response.json()
            return result
        except Exception as e:
            return ""


class TranmissionProvider(Provider):
    def get(self):
        result = ""
        for status in ["Downloading", "Seeding"]:
            bashCommand = "transmission-remote  192.168.0.101:9091 -l | head -n -1 | grep " + status + " | wc -l"

            output, error = subprocess.Popen(
                bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()

            count = int(output)
            if count > 0:
                if len(result) > 0:
                    result += ", "
                result += status + ": " + str(count)
        return result


class BashProvider(Provider):
    def __init__(self, arguments):
        self.name = arguments[0]
        self.bashCommands = arguments[1]

    def get(self):
        result = self.name

        for bashCommand in self.bashCommands:

            output, error = subprocess.Popen(
                bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ).communicate()
            result += " " + output.decode("utf-8")

        return result


class ProviderFactory:
    def new(self, type_name, args):
        if type_name == "netatmo":
            return NetatmoProvider(args)
        elif type_name == "wttrin":
            return WttrInProvider("")
        elif type_name == "transmission":
            return TranmissionProvider("")
        elif "bash" in type_name:
            return BashProvider(args)
