#!/usr/bin/python3
#coding:utf-8

import urllib
import csv
from bs4 import BeautifulSoup
from urllib.parse import quote

import station
import config

if __name__ == '__main__':
    # select city
    print('===== Choose Station =====')
    print('1 Keelung City       基隆市  2 New Taipei City 新北市    ' +
        '3 Taipei City     臺北市')
    print('4 Taoyuan City       桃園市  5 Hsinchu County  新竹縣    ' +
        '6 Hsinchu City    新竹市')
    print('7 Miaoli County      苗栗縣  8 Taichung City   臺中市    ' +
        '9 Nantou County   南投縣')
    print('10 Changhua County   彰化縣  11 Yunlin County  雲林縣    ' +
        '12 Chiayi County  嘉義縣')
    print('13 Chiayi City       嘉義市  14 Tainan City    臺南市    ' +
        '15 Kaohsiung City 高雄市')
    print('16 Pingtung County   屏東縣  17 Yilan County   宜蘭縣    ' +
        '18 Hualien County 花蓮縣')
    print('19 Taitung County    臺東縣  20 Penghu County  澎湖縣    ' +
        '21 Kinmen County  金門縣')
    print('22 Lienchiang County 連江縣')
    print('')
    cityNumber = input('County/City Number: ')
    cityName = config.cityList[cityNumber]
    print('')
    print(cityName)
    print('')

    # select station
    cityStationList = []
    count = 0
    for station in station.stationList:
        if station[5] == cityName:
            cityStationList.append([station[0], station[1]])
            print(str(count + 1) + ' ' + cityStationList[-1][0] + \
                ' ' + cityStationList[-1][1])
            count += 1
    print('')
    stationNumber = input('Station Number: ')
    stationInfo = cityStationList[int(stationNumber) - 1]
    print('')
    print(stationInfo[0] + ' ' + stationInfo[1])
    print('')

    # select date
    print('===== Select Date =====')
    print('Example: 2019-01-01')
    date = input('Date: ')
    dateInfo = date.split('-')

    # get link
    webLink = config.webLink
    webLink += '&station=' + stationInfo[0]
    webLink += '&stname=' \
        + str(urllib.parse.quote(stationInfo[1]).replace('%', '%25'))
    webLink += '&datepicker=' + date

    html = urllib.request.urlopen(webLink).read()
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'MyTable'})
    if table == None:
        print("Data DOES NOT exists!")
        raise SystemExit
    print('')

    # export data to csv file
    print('===== Data =====')
    trsItem = table.find_all('tr')[1:3]
    rowsItem = []
    for tr in trsItem:
        rowsItem.append(['Year', 'Month', 'Day'])
        rowsItem[-1].extend([th.text.replace('\t', '') \
            for th in tr.find_all('th')])

    with open('data.csv', 'w') as outFile:
        writer = csv.writer(outFile)
        print([stationInfo[0], stationInfo[1]])
        writer.writerow([stationInfo[0], stationInfo[1]])
        for i in range(2):
            print(rowsItem[i])
            writer.writerow(rowsItem[i])

        trsData = table.find_all('tr')[3:]
        rowsData = []
        for tr in trsData:
            rowsData.append([dateInfo[0], dateInfo[1], dateInfo[2]])
            rowsData[-1].extend([td.text.replace('\n', '').replace('\xa0', '')
                for td in tr.find_all('td')])
            print(rowsData[-1])
            writer.writerow(rowsData[-1])
