import json
import numpy
import datetime
import decimal
from IOTAssignmentUtilitiesdorachua.OurCustomEncoder import OurCustomEncoder


def data_to_json(data):
        json_data = json.dumps(data,cls=OurCustomEncoder)
        return json_data