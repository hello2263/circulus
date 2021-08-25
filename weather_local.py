import pandas as pd


global Location, File, user_location_x, user_location_y

Location = 'C:/python/weather_api'
File = 'location.xlsx'

print('지역을 입력해주세요. (ex - 서울특별시 관악구 행운동)')
user_location= input().split(' ')


##################################################### 엑셀파일 읽고 user x, y좌표 따기함수
def find_user_location(user_location=user_location, user_location_x = 0, user_location_y = 0):

    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)
    data_pd1 = data_pd[data_pd[0]==user_location[0]]
    data_pd2 = data_pd1[data_pd1[1]==user_location[1]]
    for item in data_pd2[2]:
        if(item==user_location[2]):
            user_location_x_list = list(data_pd2[data_pd2[2] == item][3])
            user_location_x = user_location_x_list[0]
            user_location_y_list = list(data_pd2[data_pd2[2] == item][4])
            user_location_y = user_location_y_list[0]

    if((user_location_x == 0 | user_location_y == 0) == True):
        return '지역명이 잘못 입력되었습니다.'
    else:
        return user_location_x, user_location_y
#####################################################


