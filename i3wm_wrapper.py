# -*- coding: utf-8 -*-

import json
import sys
from provider import *


class I3StatusProvider:
    """
    example input from i3status:

    {"version":1}
    [
    [{"name":"ipv6","color":"#FF0000","markup":"none","full_text":"no IPv6"}]
    <subsequent lines:>
    ,[{"name":"ipv6","color":"#FF0000","markup":"none","full_text":"no IPv6"}]
    """

    def __init__(self, providers_with_credentials):
        self.providers = {}
        factory = ProviderFactory()
        for provider_name, provider_credentials in providers_with_credentials.items():
            self.providers.update({provider_name: factory.new(provider_name, provider_credentials)})

    def constructOutputString(self):
        for line in sys.stdin:
            if line[0] == ",":
                line = line[1:]
            if '{"version":1}' != line.rstrip() and "[" != line.rstrip():
                out_json = json.loads("[]")
                try:
                    out_json = self.insertData(line)
                except Exception as e:
                    out_json.insert(0, str(e))
                sys.stdout.write(json.dumps(out_json) + ",")

            else:
                sys.stdout.write(line)

    def insertData(self, line, position=0):

        out_json = json.loads(line)
        for provider_name, provider in self.providers.items():
            data_to_insert = provider.get()
            if data_to_insert != "":
                jsonized_string = {"name": provider_name, "markup": provider_name, "full_text": data_to_insert}

                out_json.insert(position, jsonized_string)
        return out_json


i3status_provider = I3StatusProvider(
    {
        "netatmo": "/home/mihai/.netatmo-credentials.yaml",
        "wttrin": "",
        "transmission": "",
        "bash_eos": (
            "EOS:",
            ['LC_NUMERIC="C" && curl --silent rate.sx/1EOS | tr -d \'\n\' | xargs printf "%0.2f"'],
            "$",
        ),
        "bash_btc": (
            "BTC:",
            ['LC_NUMERIC="C" && curl --silent rate.sx/1BTC | tr -d \'\n\' | xargs printf "%0.0f"'],
            "$",
        ),
    }
)
i3status_provider.constructOutputString()
