from flask import Blueprint, render_template, request
from app import replica_connect
from datetime import datetime
import os
import MySQLdb
import decimal
import hashlib
import json

# Define the Blueprint
visualizer = Blueprint("visualizer", __name__,
                       url_prefix="/visualizer",
                       template_folder="templates",
                       static_folder='static')


@visualizer.route('/')
def index():
    return render_template("visualizer/charts_index.html")


@visualizer.route('/charts/<hash_link>')
def return_chart(hash_link=""):
    _filename = "{0}.html".format(hash_link)
    return render_template("charts/{0}".format(_filename))


@visualizer.route('/sql', methods=["POST"])
def parse_sql():
    if request.method == "POST":
        if len(request.form["sql"]) > 0:
            try:
                json_container = []
                sql_string = request.form["sql"]
                date_format = request.form["date_format"]
                chart_title = request.form["chart_title"]
                y_target = request.form["target_variable"]
                chart_type = request.form["chart_type"]
                prefix_symbol = request.form["prefix_symbol"]
                area_fill = request.form["area_fill"]
                cursor = replica_connect()
                cursor.execute(sql_string)
                data = cursor.fetchall()
                for row in data:
                    data_dict = dict()
                    for key in row.keys():
                        if type(row[key]) is decimal.Decimal:
                            data_dict[key] = float(row[key])
                        else:
                            data_dict[key] = row[key]
                    json_container.append(data_dict)

                # Finding the min, max, and average for the target variable
                if len(request.form["target_variable"]) > 0:
                    val_list = [x[y_target] for x in json_container]
                    target_min = min(val_list)
                    target_max = max(val_list)
                    target_avg = sum(val_list) / len(val_list)
                else:
                    target_min = 0
                    target_max = 0
                    target_avg = 0

                # Dumping the JSON container out to JSON
                chart_json = json.dumps(json_container, ensure_ascii=False)

                # Takes the hash of the data plus a timestamp to generate a permanent link back to a chart
                hash_json = json_container
                hash_json.append({"ts": str(datetime.now())})
                hash_json = json.dumps(hash_json, ensure_ascii=False)
                hash_journal = hashlib.md5()
                hash_journal.update(hash_json)
                hash_link = hash_journal.hexdigest()

                context = {"chart_data": chart_json,
                           "chart_title": chart_title,
                           "target_variable": y_target,
                           "chart_type": chart_type,
                           "date_format": date_format,
                           "target_min": target_min,
                           "target_max": target_max,
                           "target_avg": target_avg,
                           "prefix_symbol": prefix_symbol,
                           "area_fill": area_fill,
                           "hash_link": hash_link}

                # This will write out a page to save our chart to, permanently
                permanent_page = render_template("visualizer/charts.html", context=context)
                with open(os.path.join(os.getcwd(), "app/templates/charts/{0}.html".format(hash_link)), "w") as f:
                    f.write(permanent_page)

                return render_template("visualizer/charts.html", context=context)
            except MySQLdb.Error as e:
                return render_template("visualizer/sqlError.html", error=e)
        else:
            return render_template("visualizer/sqlError.html", error="You didn't enter any SQL.")