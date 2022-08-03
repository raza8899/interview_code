from data_engineer.db_connect import db_session
import humanfriendly
import json

def execute_sql_query(query):
    results = None
    with db_session() as session:
        results = session.execute(query)
        results = results.all()
    return results

# Query for average complete time of a course
AVG_COMLETE_TIME_COURSE = """
SELECT course_id, AVG(time_to_completion) as avg_course FROM 
(SELECT completed_date-start_date as time_to_completion, course_id from public.certificates) 
AS avg_table GROUP BY course_id; 
"""

# Query for average amount of users time spent in a course
AVG_USER_TIME_SPENT_IN_COURSE = """
SELECT user_id, AVG(time_spent_on_courses) as avg_time 
FROM (SELECT completed_date-start_date as time_spent_on_courses, user_id from public.certificates) 
AS time_spent_table GROUP BY user_id; 
"""

# Query for average amount of users time spent for each course individually
AVG_USER_TIME_SPENT_IN__EACH_COURSE = """
SELECT user_id, course_id, AVG(time_spent_on_courses) as avg_time FROM 
(SELECT completed_date-start_date as time_spent_on_courses, user_id, course_id from public.certificates) 
AS time_spent_table GROUP BY user_id, course_id; 
"""

# Query to get top 5 fastest and top 5 slowest users completing a course
FASTEST_SLOWEST_USERS = """
    select user_id,completed_date-start_date as time_spent_on_course from public.certificates tm where tm.id in  
           (SELECT id from public.certificates  ORDER BY completed_date-start_date ASC LIMIT 5)  OR 
           tm.id in
           (SELECT id from public.certificates  ORDER BY completed_date-start_date DESC LIMIT 5) ;
"""

# Query to get certificates per customer
COUNT_CERTFICATIONS = """
select user_id, count(id) as certifications_count from public.certificates GROUP BY user_id ORDER BY certifications_count DESC;
"""

if __name__ == "__main__":
    # each query results are also saved to a json file 
    query_results = execute_sql_query(AVG_COMLETE_TIME_COURSE)
    avg_complete_time = [ {"course_id":str(course_id), "avg_complete_time":humanfriendly.format_timespan(avg_time) } for course_id, avg_time in query_results]
    with open("data_engineer/query_results/avg_complete_time_course.json",'w') as f:
        json.dump(avg_complete_time, f, indent=4)
    
    query_results = execute_sql_query(AVG_USER_TIME_SPENT_IN_COURSE)
    user_time_spent_in_course = [ {"user_id":str(user_id), "avg_time_spent":humanfriendly.format_timespan(avg_time) } for user_id, avg_time in query_results]
    with open("data_engineer/query_results/user_time_spent_in_course.json",'w') as f:
        json.dump(user_time_spent_in_course, f, indent=4)
    
    
    query_results = execute_sql_query(AVG_USER_TIME_SPENT_IN__EACH_COURSE)
    user_avg_time_spend_individual_course = [ {"user_id":str(user_id),"course_id":str(course_id) ,
    "avg_time_spent":humanfriendly.format_timespan(avg_time) } for user_id, course_id, avg_time in query_results]
    
    with open("data_engineer/query_results/user_time_spent_in_individual_course.json",'w') as f:
        json.dump(user_avg_time_spend_individual_course, f, indent=4)
    
    query_results = execute_sql_query(FASTEST_SLOWEST_USERS)
    fastest_and_slowest_users = [ {"user_id":str(user_id), "time_spent_on_course":avg_time } for user_id, avg_time in query_results]
    fastest_and_slowest_users = sorted(fastest_and_slowest_users, key=lambda d: d['time_spent_on_course'])
    fastest_and_slowest_users = [ {** row,**{"time_spent_on_course":humanfriendly.format_timespan(row.get('time_spent_on_course'))}} for row in fastest_and_slowest_users]
    
    with open("data_engineer/query_results/fastest_slowest_users.json",'w') as f:
        json.dump(fastest_and_slowest_users, f, indent=4)
    
    
    query_results = execute_sql_query(COUNT_CERTFICATIONS)
    certification_per_user = [ {"user_id":str(user_id), "certification_count":certification_count } for user_id, certification_count in query_results]
    with open("data_engineer/query_results/certifications_per_user.json",'w') as f:
        json.dump(certification_per_user, f, indent=4)