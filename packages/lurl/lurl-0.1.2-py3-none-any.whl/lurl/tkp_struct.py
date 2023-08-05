import requests
import uncurl
import re
import urllib.parse
import pprint
import json
from .requrl import LurlRequest
import time

class TkpStruct(object):

    def __init__(self, curl_prod=None, curl_stag=None, file_id=None, additional_info=None):
        self.request_presenter = None
        if not curl_stag is None :
            self.request_stag = LurlRequest(curl_stag)
            self.request_presenter = self.request_stag
        else :
            self.request_stag = dict()
        if not curl_prod is None :
            self.request_prod = LurlRequest(curl_prod)
            self.request_presenter = self.request_prod
        else :
            self.request_prod = dict()
        self.base = None
        self.file_id = file_id
        self.additional_info = additional_info

    def get_as_tkp(self):
        self.construct()
        self.print_to_file()

    def print_to_file(self):
        path_split = self.request_presenter.path.split("/")
        path_for_file = path_split[1]
        path_split = path_split[2:]
        for sub_path in path_split :
            path_for_file = path_for_file + sub_path.capitalize()
        if not self.file_id is None:
            path_for_file = path_for_file + "_" + self.file_id
        file_name = "test_"+ self.get_service_name() + "_" + path_for_file + ".json"
        f = open(file_name, "w")
        f.write(json.dumps(self.base, indent=4, sort_keys=True))
        f.close()
        print(file_name + " has just created")

    def construct(self) :
        self.construct_base()
        self.base["structure"].append(self.get_production_structure())
        self.base["structure"].append(self.get_staging_structure())
        self.base.update(self.set_content_type(self.request_presenter.parsed.data))

    def construct_base(self) :
        self.base = {
            "queryName": self.get_queryName(),
            "serviceName": self.get_service_name(),
            "apiName": self.get_apiName(),
            "testCaseDescription": self.get_description(),
            "testCasePriority": self.get_priority(),
            "httpMethod":self.request_presenter.method,
            "headerMap":self.request_presenter.headers,
            "query":"",
            "filterKeys": [],
            "structure": []
        }

    def get_apiName(self):
        api_name = self.request_presenter.path
        return api_name
    
    def get_apiParamMap_from_query(self, request):
        query_tuple = urllib.parse.parse_qsl(request.query)
        query_dict = dict((x, y) for x, y in query_tuple)
        return query_dict

    def get_queryName(self):
        query_name = self.request_presenter.method + " : " + self.request_presenter.path
        if not self.file_id is None :
            query_name = query_name + " : " + self.file_id
        return query_name

    def get_variables(self, request):
        if self.request_presenter.method == "GET" :
            return self.get_apiParamMap_from_query(request)
        else :
            try :
                return json.loads(request.parsed.data)
            except :
                return request.parsed.data

    def get_production_structure(self):
        env_name = "production"
        return self.set_structure(env_name, self.request_prod)

    def get_staging_structure(self):
        env_name = "staging"
        return self.set_structure(env_name, self.request_stag)
    
    def get_description(self):
        if 'description' in self.additional_info :
            return self.additional_info['description']
        else :
            return "call " + self.request_presenter.path

    def get_priority(self):
        if 'priority' in self.additional_info :
            return self.additional_info['priority']
        else :
            return "P1"
    
    def get_service_name(self):
        if 'service' in self.additional_info :
            return self.additional_info['service']
        else :
            return "SERVICENAME"
    
    def set_structure(self, env_name, request) :
        if not bool(request) :
            structure = {
                "env" : env_name,
                "apiParamMap":dict(),
                "variables": dict(),
                "responseString":{},
                "responseCode":0
            } 
        else :
            request.call()
            structure = { 
                "env":env_name,
                "apiParamMap":dict(),
                "variables": self.get_variables(request),
                "responseString":request.response_content,
                "responseCode":request.response.status_code
            }
        return structure
    
    def set_content_type(self, postdata) :
        if self.check_form_data(postdata) :
            return {"contentType" : "form"}
        else :
            return {}

    def check_form_data(self, postdata):
        is_form_data = False
        try :
            first_split = postdata.split("&")
            for fd in first_split :
                is_form_data = True
                second_split = fd.split("=")
                if len(second_split) == 0 :
                    is_form_data = False
                    break
            return is_form_data
        except :
            return False





