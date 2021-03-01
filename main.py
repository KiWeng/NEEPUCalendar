import re
from datetime import datetime, timedelta

from ics import Calendar, Event
from ics.alarm import AudioAlarm

from scrapper import get_table, get_session


def build_calender(time_table, alarm=15):
    routine = {
        1 : ['00:00:00', '00:45:00'],
        2 : ['00:50:00', '01:35:00'],
        3 : ['02:00:00', '02:45:00'],
        4 : ['02:50:00', '03:35:00'],
        5 : ['05:30:00', '06:15:00'],
        6 : ['06:20:00', '07:05:00'],
        7 : ['07:30:00', '08:15:00'],
        8 : ['08:20:00', '09:05:00'],
        9 : ['10:30:00', '11:15:00'],
        10: ['11:20:00', '12:05:00'],
    }
    days = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7}

    calendar = Calendar()
    time_detail_re = re.compile(u'星期([\u4e00-\u9fa5])(\d+)-(\d+)')
    duration_re = re.compile(r'(\d+)-(\d+)')

    term_start = datetime.strptime(time_table['开始时间'], '%Y-%m-%d').date()
    term_end = datetime.strptime(time_table['结束时间'], '%Y-%m-%d').date()

    for lesson in time_table['课表信息']:
        lesson_duration = lesson['学时分布']
        start_week, end_week = duration_re.match(lesson_duration).groups()

        for time_detail in lesson['节次信息']:
            weekday, class_start, class_end = time_detail_re.match(time_detail['节次']).groups()
            for week in range(int(start_week), int(end_week)):
                if time_detail['时间类型'] == '单周':
                    if week % 2 != 1:
                        continue
                if time_detail['时间类型'] == '双周':
                    if week % 2 != 0:
                        continue

                event = Event()
                event.name, event.organizer, event.location \
                    = lesson['课程名称'], lesson['教师姓名'], time_detail['教室']
                a = AudioAlarm(trigger=timedelta(minutes=alarm))
                event.alarms.append(a)
                base_day = term_start + timedelta(weeks=week - 1, days=days[weekday] - 1)
                class_start_time = datetime.strptime(routine[int(class_start)][0], '%H:%M:%S').time()
                class_end_time = datetime.strptime(routine[int(class_end)][1], '%H:%M:%S').time()

                event.begin = datetime.combine(base_day, class_start_time)
                event.end = datetime.combine(base_day, class_end_time)
                calendar.events.add(event)

    return calendar


if __name__ == '__main__':
    # Change to your own userid and password
    userid = "2018309020226"
    password = ""

    session_id = get_session(userid, password)
    table = get_table(session_id, "20202")

    with open('my.ics', 'wt', encoding='utf-8') as f:
        f.write(str(build_calender(table)))
    # print(str(build_calender(table)))
