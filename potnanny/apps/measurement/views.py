from flask import render_template, redirect, request, session, Blueprint, \
    jsonify
from sqlalchemy.sql import func
from potnanny.extensions import db
from potnanny.apps.sensor.models import Sensor
from .models import Measurement
from .utils import ChartColor, CHARTBASE
import re
import datetime
import copy
import json

measurement = Blueprint('measurement', __name__,
                        template_folder='templates')


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@measurement.route('/', methods=['GET'])
def measurement_dashboard():
    sensors = Sensor.query.order_by(Sensor.address, Sensor.name)
    return render_template('measurement/index.html', 
                title='Dashboard',
                sensors=sensors)


@measurement.route('/measurement-icons', methods=['GET'])
@measurement.route('/measurement-icons/<measurement>', methods=['GET'])
def icons(measurement=None):
    """
    returns mappings for measurement-type, to the font-awesome classes used
    for an icon for that type
    """
    data = {
        'temperature': ['fas', 'fa-thermometer-half'],
        'humidity': ['fas', 'fa-cloud'],
        'soil-moisture': ['fas', 'fa-tint'],
        'soil-fertility': ['fas', 'fa-flask'],
        'ambient-light': ['fas', 'fa-sun'],
        'battery': ['fas', 'fa-battery-full'],
        'co2-ppm': ['fas', 'fa-brille'],  
    }
    if measurement:
        if measurement in data.keys():
            return jsonify(data[measurement])
        else:
            return jsonify(['fas', 'fa-question'])
    
    return json.dumps(data, default=datetime_converter)


@measurement.route('/measurement/sensor/<address>', methods=['GET'])
def latest_sensor(address):
    results = Measurement.query.filter(
        Measurement.sensor == address).group_by(
            Measurement.type_m).all()
    
    return json.dumps(results)

"""
@measurement.route('/measurement/type/<int:tid>/sensor/<int:sid>/latest', methods=['GET'])
def measurement_sensor_latest(tid, sid):
    result = Measurement.query.filter(
        Measurement.type_id == tid,
        Measurement.sensor_id == sid
    ).order_by(
        Measurement.date_time.desc()
    ).first()  

    return str(result)


@measurement.route('/measurement/chart/type/<int:pk>', methods=['GET'])
def measurement_chart_type(pk):
    hours = int(request.args.get('hours', default=1))
    legend_on = int(request.args.get('legend', default=0))
    dates_on = int(request.args.get('dateson', default=0))

    now = datetime.datetime.now()
    then = now - datetime.timedelta(hours=hours)

    sensors = sensors_reporting_in_range(pk, then, now)
    chart = copy.deepcopy(CHARTBASE)
    tracker = {}

    for s in sensors:
        # keep track of this sensor's position index in the chart dataset
        if s.name not in tracker:
            tracker[s.name] = len(tracker)

        if len(chart['data']['datasets']) <= tracker[s.name]:
            chart['data']['datasets'].append({})

        results = Measurement.query.filter(
            Measurement.type_id == pk,
            Measurement.sensor_id == s.id,
            Measurement.date_time.between(then,now)
        ).order_by(
            Measurement.date_time
        ).all()
        
        for row in results:
            if datetime.datetime.strftime(row.date_time, "%H:%M") not in chart['data']['labels']:
                chart['data']['labels'].append(datetime.datetime.strftime(row.date_time, "%H:%M"))

            if 'data' not in chart['data']['datasets'][tracker[s.name]]:
                chart['data']['datasets'][tracker[s.name]] = {
                    'label': s.name,
                    'data': [],
                    'fill': 'false',
                    'lineTension': 0.3,
                    'borderColor': ChartColor(tracker[s.name]).rgb_color(),
                }

            chart['data']['datasets'][tracker[s.name]]['data'].append(row.value)

    if legend_on:
        chart['options']['legend']['display'] = True

    if dates_on:
        chart['options']['scales']['xAxes'][0]['display'] = True

    return jsonify(chart)


@measurement.route('/measurement/chart/type/<int:tid>/sensor/<int:sid>/avg', methods=['GET'])
def measurement_chart_sensor_avg(tid,sid):
    days = int(request.args.get('days', default=1))
    legend_on = int(request.args.get('legend', default=0))
    dates_on = int(request.args.get('dateson', default=0))

    now = datetime.datetime.now()
    then = now - datetime.timedelta(days=days)
    tracker = {'avg': 0, 'min': 1, 'max': 2}

    # modify the base-chart, to handle avg, min, max datasets
    chart = copy.deepcopy(CHARTBASE)

    mtype = MeasurementType.query.get_or_404(tid)
    sensor = Sensor.query.get_or_404(sid)

    results = MeasurementAverage.query.filter(
        MeasurementAverage.type_id == tid,
        MeasurementAverage.sensor_id == sid
    ).filter(
        MeasurementAverage.date_time.between(then,now)
    ).all()

    for row in results:
        fields = ['avg','min','max']
        if datetime.datetime.strftime(row.date_time, "%m/%d %Hh") not in chart['data']['labels']:
                chart['data']['labels'].append(datetime.datetime.strftime(row.date_time, "%m/%d %Hh"))

        for key in fields:
            if len(chart['data']['datasets']) <= tracker[key]:
                chart['data']['datasets'].append({})

            if 'data' not in chart['data']['datasets'][tracker[key]]:
                chart['data']['datasets'][tracker[key]] = {
                    'label': key,
                    'data': [],
                    'fill': 'false',
                    'lineTension': 0.1,
                    'borderColor': ChartColor(tracker[key]).rgb_color(),
                }

            chart['data']['datasets'][tracker[key]]['data'].append(getattr(row, key))

    if legend_on:
        chart['options']['legend']['display'] = True

    if dates_on:
        chart['options']['scales']['xAxes'][0]['display'] = True

    return jsonify(chart)
"""


