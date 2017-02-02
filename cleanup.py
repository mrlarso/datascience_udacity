import unicodecsv
from datetime import timedelta as td
from datetime import datetime as dt
from collections import defaultdict as defaultdict
import numpy

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

def separate_udacity(data):
    data = data
    udacity_data = []
    for datum in data:
        if datum['is_udacity']:
            udacity_data.add(data.pop(datum))
    return udacity_data, data

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

udacity_users = set()

for enrollment in enrollments:
    if enrollment["is_udacity"]:
        udacity_users.add(enrollment['account_key'])


enrollment_num_rows, enrollment_unique_students, enrollment_num_unique_students = get_students_and_unique(enrollments)

engagement_num_rows, engagement_unique_students, engagement_num_unique_students = get_students_and_unique(daily_engagement)

submission_num_rows, submission_unique_students, submission_num_unique_students = get_students_and_unique(project_submissions)

def get_non_udacity(data):
    non_udacity = []
    for datum in data:
        if datum["account_key"] not in udacity_users:
            non_udacity.append(datum)
    return non_udacity

non_udacity_enrollments = get_non_udacity(enrollments)
non_udacity_engagement = get_non_udacity(daily_engagement)
non_udacity_submission = get_non_udacity(project_submissions)

paid_students={}
for enrollment in non_udacity_enrollments:
    if not enrollment["is_canceled"] or enrollment["days_to_cancel"] > 7:
        account_key = enrollment["account_key"]
        if account_key not in paid_students or paid_students[account_key] < enrollment["join_date"]:
            paid_students[account_key] = enrollment["join_date"]

paid_engagement_in_first_week = []
for engagement in daily_engagement:
    acckey = engagement["account_key"]
    engdate = engagement['utc_date']
    if acckey in paid_students and td(0) < engdate - paid_students[acckey] < td(7):
        paid_engagement_in_first_week.append(engagement)

epifw_nonzero = []
for engagement in paid_engagement_in_first_week:
    if engagement['total_minutes_visited'] > 0:
        epifw_nonzero.append(engagement)

epifw_nonzero = paid_engagement_in_first_week
# engagement_times_first_week = []
# for engagement in epifw_nonzero:
#     engagement_times_first_week.append(engagement['total_minutes_visited'])

# engagements_per_student = {}
# for engagement in epifw_nonzero:
#     acc_key = engagement['account_key']
#     if acc_key not in engagements_per_student:
#         engagements_per_student[acc_key] = [engagement]
#     else:
#         engagements_per_student[acc_key].append(engagement)

engagements_per_student = defaultdict(list)
for engagement in epifw_nonzero:
    acc_key = engagement['account_key']
    engagements_per_student[acc_key].append(engagement)


total_time_per_student = {}
for student in engagements_per_student:
    total_time_per_student[student] = sum([record['total_minutes_visited'] for record in engagements_per_student[student]])

average_time_per_student = numpy.mean(total_time_per_student.values())


print 'avreage', average_time_per_student
print 'standard_deviation', numpy.std(total_time_per_student.values())
print 'minimum', numpy.min(total_time_per_student.values())
print 'maximum', numpy.max(total_time_per_student.values())
