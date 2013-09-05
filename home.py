#!/usr/bin/env python
import pg, cgi
import auth_session
from db_functions import *
from cgi_functions import *
from navigation import *


print "Content-type: text/html\n"
html = ""
user_id = auth_session.session.getUserId()

# -----------------
html += "<div style='text-align:center; font-weight:bold;'>Home</div>"
html += """
<table class='box'>
 <tr><td><b>Type</b></td><td><b>Level</b></td></tr>
"""

names = dbQuery("select name from question_type group by name order by min(order_by)")
for name_row in names:
  name = name_row[0]
  html += "<tr><td>"+name+"</td>"

  html += "<td>"  
  levels = dbQuery("select id, level from question_type where name='"+name+"' order by level")
  for level_row in levels:
    question_type_id = str(level_row[0])
    level = str(level_row[1])
    # Has the current user passed this question type?
    row = dbGetRow("select expected_time, expected_num_questions from question_type where id='"+escape(question_type_id)+"'")
    expected_time = row[0]
    expected_num_questions = str(row[1])
    user_set_id = dbGetOne("select id from user_set where user_id='"+escape(user_id)+"' "+
       " and question_type_id='"+escape(question_type_id)+"' "+
       " and (end_time - start_time) < '"+escape(expected_time)+"'::interval "+
       " and all_correct "+
       " and (select count(*) from user_set_question where user_set_id=user_set.id and answered_correctly) >= "+expected_num_questions+" ")
    if user_set_id: color = "green"
    else: color = "red"
    html += "<a href='begin_set.py?question_type_id="+question_type_id+"' border=0>"
    html += "<img src='images/"+color+"_ball_"+level+".gif' border=0></a> "
  html += "</td>"  

  html += "</tr>"

html += "</td></tr></table>"



# ----- Output ------
print navHeader("home")
print html
print navFooter()

