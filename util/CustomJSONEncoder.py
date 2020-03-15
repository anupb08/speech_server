import json
import decimal
import datetime as dt
import numpy as np


class CustomJSONEncoder(json.JSONEncoder):
    """
        Custom Class for Serializing the data/object that will be passed to UI Layer / Service.
    """
    def default(self, o):
        if isinstance(o, dt.date):
            return o.isoformat()
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, np.float32):
            return round(float(o), 2)
        if isinstance(o, float):
            return round(float(o), 2)
        if isinstance(o, str):
            return str(0).replace('\\n', ' ').replace('\\r', ' ')

        return json.JSONEncoder.default(self, o)
