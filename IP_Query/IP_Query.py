from flask import Flask, render_template, request
import socket, struct
import pymysql
import json, re

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_ip():
    return render_template('ipquery-1.html')


@app.route('/query/')
def get_ip_info():
    ip = request.args.get('ip')

    result = {'city': '',
              'keywords': '',
              'Longitude': '',
              'Latitude': ''}
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
        long = socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
        sql = "select city, keywords, Longitude, Latitude from ip_v1 where %s between IP_Start and IP_End" % long
        conn = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='',
                               db='flask')
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
                'data': [{
                    'city': None,
                    'keywords': None,
                    'Longitude': None,
                    'Latitude': None
                },
                ]
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
    print(result)
    return json.dumps(result)



if __name__ == '__main__':
    app.run(debug=True)
