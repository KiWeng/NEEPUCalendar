import datetime
from enum import Enum

import pandas as pd
from bs4 import BeautifulSoup
from ics import Event, Calendar


class WeekDays(Enum):
    Monday = '星期一'
    Tuesday = '星期二'
    Wednesday = '星期三'
    Thursday = '星期四'
    Friday = '星期五'
    Saturday = '星期六'
    Sunday = '星期日'


Days = {'星期一': 1, '星期二': 2, '星期三': 3, '星期四': 4, '星期五': 5, '星期六': 6, '星期日': 7, }


def week_cleanup(week_range):
    week_range = week_range.replace('周', '')
    if week_range.find('-') != -1:
        week_range = week_range.split('-')
        ret_val = [x for x in range(int(week_range[0]), int(week_range[1]) + 1)]
    else:
        ret_val = [int(x) for x in week_range.split(',')]

    return ret_val


def neepu_calender_cleanup(html_input):
    criculums = []
    with open(html_input, 'r', encoding="utf-8") as source:
        html_table = BeautifulSoup(source, features='lxml').table
    table = pd.read_html(str(html_table).replace('<br/>', '|'))[0]
    # print(html_table)

    for ele in WeekDays:
        current_day = table[[ele.value]]
        # print(current_day)
        for block in current_day.iterrows():
            event = [block[0]]
            event += str(block[1]).split(' ')
            event = [x for x in event if x != '']
            event[2] = str(event[2]).replace('\nName:', '')
            if str(event[2]) == 'NaN':
                continue

            pos = event[0]
            day = Days[str(event[1])]
            info = [x for x in str(event[2]).split('|') if x != '']
            info[0] = week_cleanup(info[0])

            row = [pos, day]
            row += info
            criculums.append(row)
    return criculums


def curriculum_to_events(day, pos, name, location, info, week, starting_day):
    events = []
    time_table = {
        0: ['00:00:00', '01:35:00'],
        1: ['02:00:00', '03:35:00'],
        2: ['05:30:00', '07:05:00'],
        3: ['07:30:00', '09:05:00'],
        4: ['10:30:00', '12:05:00'],
    }
    # print(location)
    while starting_day.weekday() != 0:
        starting_day += datetime.timedelta(days=1)

    for wk in week:
        current_day = \
            starting_day + datetime.timedelta(weeks=wk - 1) \
            + datetime.timedelta(days=day - 1)
        e = Event()
        e.name = name
        e.begin = current_day.isoformat() + ' ' + time_table[pos][0]
        e.end = current_day.isoformat() + ' ' + time_table[pos][1]
        e.description = info
        e.location = location
        events.append(e)

    return events


if __name__ == "__main__":
    html_file = "学期课表.html"
    starting_day = datetime.date(2020, 8, 22)
    filename = "gsx.ics"
    curriculums = neepu_calender_cleanup(html_file)
    classes = []
    for lesson in curriculums:
        classes += curriculum_to_events(lesson[1], lesson[0], lesson[3], lesson[5], lesson[4], lesson[2], starting_day)

    cal = Calendar()
    for cla in classes:
        cal.events.add(cla)
    with open(filename, 'w', encoding='utf-8') as my_file:
        my_file.writelines(cal)
