import json
import datetime
import decimal

class CJsonEncoder(json.JSONEncoder):
    def dafault(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj,datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def arraytojson(array):
    return json.dumps(array, cls=CJsonEncoder)

def jsontoarray(jsonstr):
    return json.loads(jsonstr)