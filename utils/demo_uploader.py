#!/usr/bin/python
# -*- coding: utf-8 -*-
import calendar
import json
import pytz
import time
from datetime import timedelta
from dateutil import parser
import getpass
import urllib, urllib2, base64
import requests


class SeriesClient():

    def __init__(self):
        self.tz = pytz.timezone('Asia/Shanghai')

    # def time_series(self, start_utc, end_utc, interval = 3600):
    #     timestamp_upload = []
    #     time_download = []
    #     start_local = start_utc
    #     for item in range(start_utc, end_utc + interval, interval):
    #         timestamp_upload.append(item)
    #         time_download.append(time.strftime('%Y-%m-%d %H:%M:%S', \
    #                                   start_local.timetuple()))
    #         start_local = start_local + timedelta(seconds = interval)

    #     timestamp = [timestamp_upload, time_download]

    #     return timestamp

    def checking_eu_availability(self, energy_unit_id):
        values = {"isExternalRequest": True, "isHTMLResponseRequired": True, "energy_unit_id": energy_unit_id}
        data = urllib.urlencode(values)
        # data = values
        url = "http://localhost:8000/api/eu/"

        is_available = self.sendingRequestToDB(url, data)
        return is_available

    def sendingRequestToDB(self, url, data):
        try:
            login = 'demouser'
            password = 'demouser'
            base64string = base64.encodestring('%s:%s' % (login, password)).replace('\n', '')
            print(base64string)

            additional = {'User-Agent': 'Mozilla/5.0', 'Authorization': 'Basic %s' % base64string }
            req = urllib2.Request(url, data, additional)
            result = urllib2.urlopen(req).read()
            print result
            return result

        except Exception, e:
            print(e)


    def upload_data(self, startTime, endTime, interval, energy_unit_id):

        timestamp = range(start_utc, end_utc + interval, interval)

        #self.time_series(startTime, endTime, interval)[0]
        data = range(25)
        for index, item in enumerate(data):
            data[index] = 2*item + 3*item**2 + 1
        print data

        points = []
        for index, value in enumerate(data):
            point = [timestamp[index], value]
            points.append(point)

#        v = [{"name": '', "columns": columns, "points": points}]
#        v = json.dumps(v)
        while True:
            try:
                # self.client.write_points(json.dumps(v), 's', 5000)
                # print "Success to upload " + item
                # break
                values = {'isExternalRequest': True, 'points': points, 'time_format': 's', 'max_rows': 5000 , 'erase_flag': False}
                data = urllib.urlencode(values)

                url = "http://localhost:8000/api/putseries/"+energy_unit_id+"/"

                self.sendingRequestToDB(url, data)
                print "Success to upload "
                break
            except:
                print "Failed to add, sleep 10s"
                time.sleep(10)
        return None

    def download_data(self, energy_unit_id, start_utc, end_utc, time_format='s', interval='auto', operation='mean'):
        try:
            values = {'isExternalRequest': True, 'start_utc': str(start_utc) , 'end_utc': str(end_utc), 'time_format': time_format, 'interval': interval, 'operation': operation}
            data = urllib.urlencode(values)

            url = "http://localhost:8000/api/getseries/"+energy_unit_id+"/"

            results = self.sendingRequestToDB(url, data)
            results = json.loads(results)
        except:
            print "Failed to download"
            return

        return results

def convert_time_to_utc(timeStr):
    # default timezone is Shanghai
    parsedStr = parser.parse(timeStr)

    return calendar.timegm(parsedStr.utctimetuple())


if __name__ == "__main__":

    energy_unit_id = '83'

    start_utc = convert_time_to_utc('2015-12-14 00:00:00 +8')
    end_utc = convert_time_to_utc('2015-12-15 00:00:00 +8')
    interval = 3600


#    test_login()

    sclient = SeriesClient()
    #checking if eu is available
    # is_eu_available = sclient.checking_eu_availability(energy_unit_id)
    # if is_eu_available == "True":

    sclient.upload_data(start_utc, end_utc, interval, energy_unit_id)
    data = sclient.download_data(energy_unit_id, start_utc, end_utc)

    print data



