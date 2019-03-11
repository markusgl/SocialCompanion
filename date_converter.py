from datetime import timedelta
import datetime
from fuzzywuzzy import fuzz
import re


class DateConverter:
    @staticmethod
    def convert_relativedate(relativedate):
        appointment_end_time = 0
        if relativedate == 'heute':
            appointment_start_time = datetime.datetime.now()
        elif relativedate == 'morgen':
            appointment_start_time = datetime.datetime.now() + timedelta(days=1)
        elif relativedate == 'übermorgen':
            appointment_start_time = datetime.datetime.now() + timedelta(days=2)
        else:
            appointment_start_time = ""

        return appointment_start_time, appointment_end_time

    @staticmethod
    def convert_dateperiod(dateperiod):
        # check the fuzzy ratio (edit distance with respect of the length) of the two terms
        if fuzz.ratio(dateperiod, 'nächste tage') > 85 or fuzz.ratio(dateperiod, 'nächste zeit') > 85:
            appointment_start_time = datetime.datetime.now()
            appointment_end_time = 4
        elif fuzz.ratio(dateperiod, 'wochenende') > 85:
            # calculate days until weekend depending on weekday
            weekno = datetime.datetime.now().weekday()
            if weekno < 4:
                delta = 4 - weekno
                appointment_start_time = datetime.datetime.now() + timedelta(days=delta)
            else:
                appointment_start_time = datetime.datetime.now()

            #appointment_end_time = appointment_start_time + timedelta(days=2)
            appointment_end_time = 2
        elif fuzz.ratio(dateperiod, 'diese woche') > 85:
            weekno = datetime.datetime.now().weekday()
            delta = 6 - weekno
            appointment_start_time = datetime.datetime.now()
            appointment_end_time = delta
        else:
            appointment_start_time = 0
            appointment_end_time = 0

        return appointment_start_time, appointment_end_time

    def convert_date(self, date_string, date_type):
        """
        converts a date as string into a datetime object
        :param date_string: date as string in any format (e. g. heute, morgen, 1.1. etc.)
        :param date_type: type of the given date
        :return: date as datetime object
        """

        converted_date = ""
        if date_type == 'relativedate':
            rel_date = date_string
            if rel_date == "heute":
                time_delta = 0
            elif rel_date == "morgen":
                time_delta = 1
            elif rel_date == "übermorgen":
                time_delta = 2

            # search depending on weekday
            if "montag" in rel_date:
                time_delta = self.convert_weekay(0)
            elif "dienstag" in rel_date:
                time_delta = self.convert_weekay(1)
            elif "mittwoch" in rel_date:
                time_delta = self.convert_weekay(2)
            elif "donnerstag" in rel_date:
                time_delta = self.convert_weekay(3)
            elif "freitag" in rel_date:
                time_delta = self.convert_weekay(4)
            elif "samstag" in rel_date:
                time_delta = self.convert_weekay(5)
            elif "sonntag" in rel_date:
                time_delta = self.convert_weekay(6)
            else:
                time_delta = 0
            converted_date = datetime.datetime.now() + timedelta(days=time_delta)
            converted_date = converted_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # if date is given as numbers
        if date_type == 'date':
            # extract dateformat from string
            match = re.search(r'[0-9]{1,2}\.[0-9]{1,2}(\.)?([0-9]{4}|[0-9]{2})?', date_string)
            if match:
                # print(match.group())
                date_array = str(match.group()).split('.')
            else:
                print('No match')
                date_array = ""

            # convert different possible date format to one equal
            if len(date_array) == 2:
                day = date_array[0].zfill(2)
                month = date_array[1].zfill(2)
                year = datetime.datetime.now().year

            elif len(date_array) == 3 and date_array[2] == "":
                day = date_array[0].zfill(2)
                month = date_array[1].zfill(2)
                year = datetime.datetime.now().year

            elif len(date_array) == 3:
                day = date_array[0].zfill(2)
                month = date_array[1].zfill(2)
                if len(date_array[2]) == 4:
                    year = date_array[2]
                elif len(date_array[2]) == 2:
                    year = '20' + date_array[2]

            converted_date = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d')
            # print(type(converted_date))

        return converted_date

    def convert_weekay(self, week_no):
        """
        calculates the time gap from today to a given day depending on the week number (monday = 0, tuesday = 1, ...)
        it also recognizes if the date is in the following week or in the current
        :param week_no:
        :return:
        """
        current_weekno = datetime.datetime.now().weekday()
        if week_no <= current_weekno:  # following week
            rest_week = 7 - current_weekno
            time_delta = rest_week + week_no
        else:
            time_delta = week_no - current_weekno

        return time_delta

    def convert_time(self, time_string):
        """
        extracts the time of a string and returns the hours and minutes
        :param time_string:
        :return: hour and minute
        """
        hour = 0
        minute = 0
        # extract time from string
        match = re.search(r'[0-9]{1,2}(:|\.)?([0-9]{1,2})?', time_string)
        if match:
            time_string = match.group()
            time_array = re.split('(\.|:)', time_string)
        else:
            return

        if len(time_array) == 1:
            hour = time_array[0].zfill(2)
            minute = '00'
        elif len(time_array) == 3:
            hour = time_array[0].zfill(2)
            minute = time_array[2].zfill(2)

        return hour, minute