import requests
import uncurl
import re
import urllib.parse
import pprint
import json

class LurlRequest(object):

    def __init__(self, curl):
        self.curl = curl
        self.parsed = uncurl.parse_context(self.curl)
        self.request = uncurl.parse(self.curl)
        self.request_body = self.parsed.data
        self.method = self.parsed.method.upper()
        self.headers = dict(self.parsed.headers)
        self.query = ""
        self.path = ""
        self.parse_url()
        self.response = ""
        self.response_content = ""

    def parse_url(self):
        endpoint = re.findall("^http.*//[^/]*(/.*?)$", self.parsed.url)
        if len(endpoint) > 0 : 
            endpoint = endpoint[0]
        else :
            endpoint= "/"
        endpoint_split = endpoint.split("?",1)
        self.path = endpoint_split[0]
        if len(endpoint_split) > 1 :
            self.query = endpoint_split[1]
    
    def call(self):
        self.response = eval(self.request)
        self.response_content = self.response.text
        self.try_convert_as_json()
    
    def try_convert_as_json(self):
        try:
            self.response_content = json.loads(self.response.text)
        except:
            pass





