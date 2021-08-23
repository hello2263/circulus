from urllib.request import urlopen, Request
from urllib.parse import urlencode, unquote, quote_plus
# quote - URL에 있는 한글을 자동으로 아스키 값으로 변환시킴
# unquote - 반대로 사람이 읽을 수 있는 값으로 변환시킴
import datetime
from datetime import date, datetime, timedelta
import json
import pymysql
# import pandas as pd

db_user = "root"
db_password = "qwe123"

def db_connecting(id, key):
    global db, cursor
    db = pymysql.connect(host='127.0.0.1',
                         user=id, password=key, charset="utf8", port=5000)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute('USE test;')
    if (cursor.execute("show status like 'Threads_connected';") == 1):
        print('test_db Connected')

now = datetime.now()

today_date = str(now.year)+'0'+str(now.month)+str(now.day)
today_hour = now.hour - 1
today_minute = '00'
# if (now.minute > 50):
#     today_minute = '00'
# else:
#     today_minute = '00'
#     today_hour -= 1

CallBackURL = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
params = '?' + urlencode({
    quote_plus("serviceKey"): 'XIjRFoewvUDp4EDhRpATADoatwElkiQ%2F1J0tDooGjBTKStjRtuW3Zu89iE9cBsK%2Bz299IJwkbaE%2F%2F7SzcVo2yA%3D%3D',
    quote_plus("numOfRows"): '40',
    quote_plus('pageNo'): '1',
    quote_plus('dataType'): 'JSON',
    quote_plus('base_date'): today_date,
    quote_plus('base_time'): '1500',
    # quote_plus('base_time'): str(today_hour)+today_minute,
    quote_plus('nx'): '59',
    quote_plus('ny'): '125'
})

# URL 데이터 파싱
request = Request(CallBackURL + unquote(params))

# API를 통해 데이터 GET
response_body = urlopen(request).read()

# JSON으로 변환
data = json.loads(response_body)
item_data=data['response']['body']['items']['item']

# Pandas_DataFrame으로 출력
# table = pd.DataFrame(data['response']['body']['items']['item'])
# print(table)

weather_data = dict() # 조회한 오늘 날씨 정보

for item in item_data:
    if item['fcstTime'] == str(now.hour)+today_minute:

        if item['category'] =='T1H': # 기온체크
            weather_data['기온'] = item['fcstValue']

        if item['category'] == 'PTY': # 상태체크
            weather_code = item['fcstValue']

            if weather_code == '1':
                weather_state = 'rain'
            elif weather_code == '2':
                weather_state = 'rain or snow'
            elif weather_code == '3':
                weather_state = 'snow'
            elif weather_code == '5':
                weather_state = 'mist'
            elif weather_code == '6':
                weather_state = 'mist or snowing'
            elif weather_code == '7':
                weather_state = 'snowing'
            else:
                weather_state = 'none'

            weather_data['상태'] = weather_state

        if item['category'] == 'SKY': # 하늘체크
            weather_code = item['fcstValue']

            if weather_code == '1':
                weather_state = 'sunny'
            elif weather_code == '3':
                weather_state = 'cloudy'
            elif weather_code == '4':
                weather_state = 'gray'
            else:
                weather_state = 'none'

            weather_data['하늘'] = weather_state

data['weather'] = weather_data

db_connecting(db_user, db_password)
print(weather_data)

print("INSERT INTO weather_db(time, state, sky, tmp) VALUES ('"+str(now.hour)+str(now.minute)+"', '"+
               weather_data['상태']+"', '"+weather_data['하늘']+"', '"+weather_data['기온']+"')")

# cursor.execute("INSERT INTO weather_db(time, state, sky, tmp) VALUES ('"+str(now.hour)+str(now.minute)+"', '"+
#                weather_data['상태']+"', '"+weather_data['하늘']+"', '"+weather_data['기온']+"')")

db.commit()
db.close()
print(now.year, '년', now.month, '월', now.day, '일', now.hour, '시\n현재 관악구 날씨는' )
print(data['weather'])



