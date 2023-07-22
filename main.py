from flask import Flask, request
import re
from db import get_reading, add_reading, Reading, database
from datetime import datetime

app = Flask(__name__)


@app.post("/data")
def post_data():
    if request.content_type == 'text/plain':
        data = request.data.decode('utf-8')

        # validate data
        lines = data.split('\n')
        pattern = r'^\d+ (Voltage|Current) \d+(\.\d+)?$'
        valid_lines = []
        for line in lines:
            if line.strip() and re.match(pattern, line):
                valid_lines.append(line)
            else:
                return {"success": False}

        # insert validated data
        for valid_line in valid_lines:
            timestamp_str, name, value_str = valid_line.split()
            timestamp = int(timestamp_str)
            dt_object = datetime.utcfromtimestamp(timestamp)
            formatted_date = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            reading_obj = Reading(time=formatted_date, name=name, value=float(value_str))
            add_reading(formatted_date, reading_obj)
    else:
        return {"success": False}

    return {"success": False}


@app.get("/data")
def get_data():
    from_date_str = request.args.get('from')
    to_date_str = request.args.get('to')

    if not from_date_str or not to_date_str:
        return "Invalid request"

    from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
    to_date = datetime.strptime(to_date_str, "%Y-%m-%d")

    results = []
    for key, data in database.items():
        timestamp_date = data['timestamp']
        if from_date <= timestamp_date <= to_date:
            results.append(data)

    return results


if __name__ == "__main__":
    app.run()
