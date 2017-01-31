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
    record['account_key'] = record.pop('acct')

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

def get_students_and_unique(data):
    num_rows = len(data)
    unique_students = set(datum['account_key'] for datum in data)
    num_unique_students = len(unique_students)
    return num_rows, unique_students, num_unique_students

enrollment_num_rows, enrollment_unique_students, enrollment_num_unique_students = get_students_and_unique(enrollments)

engagement_num_rows, engagement_unique_students, engagement_num_unique_students = get_students_and_unique(daily_engagement)

submission_num_rows, submission_unique_students, submission_num_unique_students = get_students_and_unique(project_submissions)


print 'enrollment', enrollment_num_unique_students
print 'engagment', engagement_num_unique_students
print 'sumission', submission_num_unique_students
