import requests
import json


def httpget(url, paramsDict=None):
    '''
    http get
    '''
    if paramsDict is None:
        response = requests.get(url=url)
        return response.text
    response = requests.get(url=url, params=paramsDict)
    return response.text


def httppost_form(url, data):
    '''
    http post application/x-www-form-urlencoded

    - par:
        - url str
        - data dict
    '''
    response = requests.post(url=url, data=data, headers={
                             'Content-Type': 'application/x-www-form-urlencoded'})
    return response.text


def httppost_json(url, data):
    '''
    http post application/json

    - par:
        - url str
        - data dict
    '''
    response = requests.post(url=url, data=json.dumps(data), headers={
                             'Content-Type': 'application/json'})
    return response.text


def httppost_xml(url, xml):
    '''
    http post text/xml

    - par:
        - url str
        - xml str <?xml  ?>
    '''
    response = requests.post(url=url,data=xml,headers={'Content-Type':'text/xml'})
    return response.text
