# Work08 (IoT Device Programming 3 Week 8)
# Group 3
# Created by Shotar Noda(TK220137) on 2024/07/05.

from flask import Flask, request, render_template
import csv

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
  data_list = []
  total_temperature = 0
  total_humidity = 0
  count = 0

  print(f"ACCESS HOST:{request.remote_addr}")
  
  path = "./data/20240705.csv"
  
  try:
    with open(path) as f:
      reader = csv.reader(f)
      for row in reader:
        print(f">Row: {row}")
        data_list.append(row)
        if len(row) >= 2:
                    try:
                        total_temperature += float(row[0])
                        total_humidity += float(row[1])
                        count += 1
                    except ValueError:
                        continue
  except FileNotFoundError:
    data_list = [["-", "-"]]
  avg_temperature = total_temperature / count if count > 0 else 0
  avg_humidity = total_humidity / count if count > 0 else 0


  return render_template('main.html',
                         title="DevPro3",
                         name="User",
                         data_list=data_list,
                         avg_temperature=avg_temperature,
                         avg_humidity=avg_humidity,
                         max_value=len(data_list))
  @app.route("/", methods=["POST"])
def index2():
    text_from_html = request.form['new_tempe']
    print(text_from_html)
    #
    #
    return render_template("index.html") 
    # example41 is being used.

if __name__ == "__main__":
  app.run(host = '0.0.0.0', port = 5001, debug=True)
