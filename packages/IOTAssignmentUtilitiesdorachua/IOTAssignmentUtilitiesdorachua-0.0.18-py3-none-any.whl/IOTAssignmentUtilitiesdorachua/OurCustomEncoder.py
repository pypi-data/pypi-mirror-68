import json
import numpy
import datetime
import decimal

class OurCustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if obj is None:
            return str("")
        #elif isinstance(obj, None):
        #     return str("None")
        elif isinstance(obj, numpy.generic):
            return numpy.asscalar(obj) 
        elif isinstance(obj, datetime.datetime):  
            #ISO 8601 — 2014-12-06T10:30:00-0800.
            return obj.strftime('%Y-%m-%dT%H:%M:%S+0800') 
        elif isinstance(obj, decimal.Decimal)   :
            return float(obj)
        elif isinstance(obj, float.__float__):
            return float(obj)            
        return json.JSONEncoder.default(self, obj)