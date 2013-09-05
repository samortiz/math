#!/usr/bin/env python
import pg, cgi
import auth_session
from db_functions import *
from cgi_functions import *
from navigation import *
from misc_functions import *

print "Content-type: text/html\n"
html = ""
user_id = auth_session.session.getUserId()

# -----------------
html += "<div style='text-align:center; font-weight:bold;'>High Scores</div>"
html += """
<table class='box' cellpadding=2px>
 <tr>
  <td><b>Type</b></td>
  <td style='padding-left:20px;'><b>Best Time</b></td>
  <td style='padding-left:20px;'><b>Your Time</b></td>
 </tr>
"""

names = dbQuery("select id, name||' level '||level from question_type order by order_by")
for name_row in names:
  question_type_id = name_row[0]
  name = name_row[1]

  # Get the best time
  row = dbGetRow("""
    select u.nickname
         , extract('days' from (us.end_time - us.start_time)) as days 
         , extract('hours' from (us.end_time - us.start_time)) as hours 
         , extract('minutes' from (us.end_time - us.start_time)) as minutes
         , extract('seconds' from (us.end_time - us.start_time)) as seconds
    from user_set us
       , users u 
    where us.question_type_id='"""+str(question_type_id)+"""' 
      and u.id = us.user_id
      and us.all_correct = true
    order by (us.end_time - us.start_time) asc
     """) 
  user_name = ""
  bestTime = ""
  if row:
    user_name = row[0]
    days = row[1]
    hours = row[2]
    mins = row[3]
    secs = row[4]
    bestTime = formatIntervalShort(days, hours, mins, secs)

  # Get your best time
  row = dbGetRow("""
    select extract('days' from (us.end_time - us.start_time)) as days 
         , extract('hours' from (us.end_time - us.start_time)) as hours 
         , extract('minutes' from (us.end_time - us.start_time)) as minutes
         , extract('seconds' from (us.end_time - us.start_time)) as seconds
    from user_set us
       , users u 
    where u.id='"""+str(user_id)+"""'
      and us.question_type_id='"""+str(question_type_id)+"""' 
      and u.id = us.user_id
      and us.all_correct = true
    order by (us.end_time - us.start_time) asc
     """)
  yourTime = ""
  if row:
    days = row[0]
    hours = row[1]
    mins = row[2]
    secs = row[3]
    yourTime = formatIntervalShort(days, hours, mins, secs)

  html += "</td>"  
  html += "<tr>"
  html += "<td>"+name+"</td>"
  html += "<td style='padding-left:20px;'>"+user_name+" "+bestTime+"</td>"  
  html += "<td style='padding-left:20px;'>"+yourTime+"</td>"
  html += "</tr>"

html += "</td></tr></table>"



# ----- Output ------
print navHeader("highscores")
print html
print navFooter()

