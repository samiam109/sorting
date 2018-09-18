import json
import csv
import datetime
from dateutil import parser
from dateutil.rrule import *


class DateCounter:

    NOW = datetime.datetime.date(datetime.datetime.now())
    NOW_YEAR = NOW.year
    DATES = []
    date = ""
    # create list with all available dates in a year
    THIS_YEAR_DATES = list(rrule(DAILY, dtstart=parser.parse(str(NOW_YEAR)+"0101"), until=NOW))
    DAILY_COUNTS = {}
    DAY_IPS = {}

    def utc_to_local(utc_dt):
        """
        :param utc_dt: datetime object in utc tz
        :return: datetime object containing utc_dt converted to local dt
        """
        return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)

    # convert from file to list of strings
    with open("login.log", "r") as logf:
        SAMPLE = logf.readlines()

    # convert from list of strings to list of json
    for i, r in enumerate(SAMPLE):
        r = json.loads(r)
        SAMPLE[i] = r
        time = SAMPLE[i].get("time")
        SAMPLE[i]["time"] = utc_to_local(parser.parse(time))  # replace tz with local tz in dt object format

    for object in SAMPLE:
        if object["uri"] in "/user/login":
            DATES.append((object["time"].date(), object["remote_ip"]))

    def organize_login_requests(self):
        for date in self.THIS_YEAR_DATES:
            # print("DATE: ", date.date())
            ips_in_day = {}
            count_for_day = 0
            for login in self.DATES:
                # print("LOGIN:  ", login)
                if date.date() == login[0]:

                    if login[1] not in ips_in_day:
                        ips_in_day[login[1]] = 1
                        count_for_day += 1
                    else:
                        ips_in_day[login[1]] += 1
                        count_for_day += 1

            if count_for_day > 1:
                self.DAILY_COUNTS[str(date.date())] = ips_in_day
                self.DAILY_COUNTS[str(date.date())+"Count"] = count_for_day

    def write_json_file(self, confirm=False):
        if confirm is True:
            with open("Daily_active_users.json", "w+") as jf:
                jf.write(json.dumps(self.DAILY_COUNTS))

    def write_csv_file(self, confirm=False):
        print(confirm)
        if bool(confirm) is True:
            with open("Daily_user_login.csv", "w+") as csvf:
                csv_writer = csv.writer(csvf)
                csv_writer.writerow(("Date", "Count"))
                csv_writer.writerows(self.DAILY_COUNTS.items())


temp = DateCounter()
temp.organize_login_requests()
temp.write_csv_file(1)
