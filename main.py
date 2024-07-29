# Work08 (IoT Device Programming 3 Week 8)
# Group 3
# Created by Shotar Noda(TK220137) on 2024/07/22.

from flask import Flask, request, render_template
import csv, datetime

app = Flask(__name__)

## Index
@app.route("/", methods=["GET"])
def index():
  data_list = []
  total_temperature = 0
  total_humidity = 0
  count = 0

  print(f"ACCESS HOST:{request.remote_addr}")
  
  path = "./data/dummy_data.csv"
  
  try:
    with open(path) as f:
      reader = csv.reader(f)
      collected_data = [row for row in reader]
      del collected_data[0] # ヘッダー行は不要なので削除する
  
      for row in collected_data:
        print(f">Row: {row}")
        data_list.append(row)
        if len(row) >= 2:
          try:
              dt = datetime.datetime.fromtimestamp(row[1])
              row[1] = dt.replace(second=0, microsecond=0)
              total_temperature += float(row[2])
              total_humidity += float(row[3])
              count += 1
          except ValueError:
              continue
  except FileNotFoundError:
    data_list = [["-", "-"]]
  avg_temperature = round(total_temperature / count, 2) if count > 0 else 0
  avg_humidity = round(total_humidity / count, 2) if count > 0 else 0
  
  return render_template('index.html',
                         title="DevPro3",
                         name="User",
                         data_list=data_list,
                         avg_temperature=avg_temperature,
                         avg_humidity=avg_humidity,
                         max_value=len(data_list))

## データ追加API
@app.route("/api/add_data", methods=["POST"])
def add_data():
    new_tempe = request.form.get('new_tempe')
    if new_tempe:
        print(f"New temperature: {new_tempe}")
        write_csv("./data/dummy_data.csv", [new_tempe])
    return "Temperature data has been written to the CSV file."
  
def write_csv(path1, data):
    with open(path1, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

if __name__ == "__main__":
  app.run(host = '0.0.0.0', port = 5001, debug=True)
