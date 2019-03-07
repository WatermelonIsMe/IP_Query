from flask import Flask, render_template, request
import socket, struct
import pymysql
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_ip():
    return render_template('iptest.html')


@app.route('/query', methods=['POST'])
def get_ip_info():
    ip = eval(request.data).get('ip')
    result = {'city': '',
              'keywords': '',
              'Longitude': '',
              'Latitude': ''}
    if ip:
        long = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
        sql = "select city, keywords, Longitude, Latitude from test where %s >= IP_Start and %s <= IP_End" % (
            long, long)
        conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='flask')
        cur = conn.cursor()
        cur.execute(sql)
        tmp = cur.fetchone()
        if tmp:
            result = {
                'status': 'success',
                'code': 200,
                'data': {
                    'city': tmp[0],
                    'keywords': tmp[1],
                    'Longitude': tmp[2],
                    'Latitude': tmp[3]
                }
            }
        else:
            result = {
                'status': 'fail',
                'code': 404,
                'data': {
                    'city': None,
                    'keywords': None,
                    'Longitude': None,
                    'Latitude': None
                }
            }
    else:
            result = {
                'status': 'fail',
                'code': 400,
                'data': {
                    'city': None,
                    'keywords': None,
                    'Longitude': None,
                    'Latitude': None
                }
            }
    return json.dumps(result)


if __name__ == '__main__':
    app.run('0.0.0.0',5002,debug=True)
