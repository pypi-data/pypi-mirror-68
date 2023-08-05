import os
from Naked.toolshed.shell import muterun_js
from collections import OrderedDict

def get_curls(har_folder_path):
    curl_string_list = get_curl_string_list(har_folder_path)
    curls = OrderedDict()
    for curl_string in curl_string_list :
        curl, file_id = get_curl_and_file_id(curl_string)
        curls[file_id] = curl
    return curls

def get_curl_string_list(har_folder_path):
    response = muterun_js(get_hartocurl_file() + ' "' + har_folder_path + '"')
    curl_string_list = list()
    if response.exitcode == 0:
        curl_string_list = response.stdout.decode('utf-8').splitlines()
    else :
        print(response.stderr)
    return curl_string_list

def get_file_id(path_string):
    file_id = path_string
    try:
        file_id = file_id.rsplit('/',1)[1]
    except:
        pass
    return file_id


def get_curl_and_file_id(response_string):
    response_split = response_string.split("---",1)
    curl_string = response_split[1]
    file_id = get_file_id(response_split[0])
    return curl_string, file_id

def get_hartocurl_file():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'harcurl.js')