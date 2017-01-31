import unicodecsv
from datetime import datetime as dt

def read_csv(filename):
    with open(filename, 'rb') as f:
        data = unicodecsv.DictReader(f)
        return list(data)

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')

def parse_date(date):
    if date == "":
        return None
    return dt.strptime(date, '%Y-%m-%d')

def parse_maybe_int(i):
    if i == "":
        return None
    return int(i)

for enrollment in enrollments:
    enrollment['join_date'] = parse_date(enrollment['join_date'])
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])

for record in daily_engagement:
    record['lessons_completed'] = int(float(record['lessons_completed']))
    record['num_courses_visited'] = int(float(record['num_courses_visited']))
    record['total_minutes_visited'] = float(record['total_minutes_visited'])
    record['projects_completed'] = int(float(record['projects_completed']))
    record['utc_date'] = parse_date(record['utc_date'])

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])
