# Work10 (IoT Device Programming 3 Week 13)
# Group 3
# Created by Shotar Noda(TK220137) on 2024/07/29.

import socket, os, threading, json, fasteners
from datetime import timedelta, timezone, datetime
from dotenv import load_dotenv
load_dotenv()

def socket_receiver(connection, address, lock):
  print(f"[{get_current_date()}]Connection from {str(address)} has been established.")
  data_receive = connection.recv(4096)
  data_decoded = data_receive.decode('utf-8')
  data_json = json.loads(data_decoded)
  
  data_listed = []
  for i in range(len(data_json)):
      print(data_json[i])
      single_data = data_json[i]
      data_listed.append([single_data["hostname"],
                          single_data["timestamp"],
                          single_data["temp_dht"],
                          single_data["humid_dht"]])
      
  lock.acquire()
  save_csv(data_listed)
  lock.release()
  print(f"[{get_current_date()}]CSV saved.")

## 日時取得関数
def get_current_date():
  return datetime.now(timezone(timedelta(hours=+9), 'Asia/Tokyo'))

## CSV保存関数
def save_csv(list_data):
  with open(f'data/dummy_data.csv', mode="a") as f:
    for row in list_data:
      print(*row, sep=',', file=f)
  f.close()

if __name__ == '__main__':
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
  sock.bind((os.getenv('SERVER_ADDR'), int(os.getenv('WAITING_PORT'))))
  sock.listen(int(os.getenv('MAX_CLIENT')))
  
  sock.settimeout(0.5)
  
  lock = fasteners.InterProcessLock('/var/tmp/lockfile')
  
  while True:
    try:
      conn, addr = sock.accept()
      if conn:
        thread = threading.Thread(target=socket_receiver, args=(conn, addr, lock), daemon=True)
        thread.start()
    except KeyboardInterrupt:
      sock.close()
      print(f"[{get_current_date()}]Server Stopped.")
      exit()
    except socket.timeout:
      continue
    except Exception as e:
      sock.close()
      print(e)
      exit()