#!/usr/bin/env python
import pg, cgi
import auth_session
from db_functions import *
from cgi_functions import *
from navigation import *
from misc_functions import *

print "Content-type: text/html\n"
html = ""

# ----Get the result data ----
user_set_id = getParam("user_set_id")

row = dbGetRow(
 "select qt.name "+
 "     , extract('days' from (us.end_time - us.start_time)) as days "+
 "     , extract('hours' from (us.end_time - us.start_time)) as hours "+
 "     , extract('minutes' from (us.end_time - us.start_time)) as minutes "+
 "     , extract('seconds' from (us.end_time - us.start_time)) as seconds "+
 "     , qt.id "+
 "from user_set us "+
 "   , question_type qt "+
 "where us.question_type_id=qt.id "+
 "  and us.id='"+escape(user_set_id)+"'")

question_type_name = row[0]
timeHtml = formatInterval(row[1], row[2], row[3], row[4])
question_type_id = str(row[5])

num_correct = dbGetOne("select count(*) from user_set_question where user_set_id='"+escape(user_set_id)+"' and answered_correctly=true")
num_questions = dbGetOne("select count(*) from user_set_question where user_set_id='"+escape(user_set_id)+"'")
percentage = (float(num_correct) / float(num_questions)) * 100
percentage_str = "%.0f" % percentage

#Expectations to pass
row = dbGetRow("select expected_time, expected_num_questions from question_type where id='"+escape(question_type_id)+"'")
expected_time = row[0]
expected_num_questions = str(row[1])
passed_level = dbGetOne("select id from user_set where id='"+escape(user_set_id)+"' "+
       " and (end_time - start_time) < '"+escape(expected_time)+"'::interval and all_correct "+
       " and (select count(*) from user_set_question where user_set_id=user_set.id and answered_correctly) >= "+expected_num_questions+" ")
if passed_level:
  passHtml = "<tr><td><font color='green'>Congratulations you passed this level!</font></td></tr>"
else:
  passHtml = ""


# -------------- Draw the content ----------------

html += "<table class='centered' border=0 cellspacing=0 cellpadding=0>"
html += "<tr><td align=center><b>Results</b></td></tr>"
html += "<tr><td>Time: "+timeHtml+"</tr></td>"
html += "<tr><td>Score: "+num_correct+" / "+num_questions+" ("+percentage_str+"%) </td></tr>"
html += "<tr><td>Time Limit: "+expected_time+"</td></tr>"
html += "<tr><td>"+passHtml+"</td></tr>"
html += "<tr><td><a href='begin_set.py?question_type_id="+question_type_id+"'>Do this set again</a></td></tr>"
html += """
<tr><td>
<table class='box' border=1 style='border-collapse:collapse' cellspacing=0 cellpadding=3 width=100%>
<tr>
 <th>#</th>
 <th>Question</th>
 <th>Answer</th>
 <th>Time</th>
</tr>
"""
setResults = db.query("""
select usq.answered_correctly
     , extract('days' from (usq.end_time - usq.start_time)) as days
     , extract('hours' from (usq.end_time - usq.start_time)) as hours
     , extract('minutes' from (usq.end_time - usq.start_time)) as minutes
     , extract('seconds' from (usq.end_time - usq.start_time)) as seconds
     , usq.answer
     , usq.answer2
     , usq.answer3
     , usq.answer4
     , q.correct_answer
     , q.correct_answer2
     , q.correct_answer3
     , q.correct_answer4
     , q.question_text
     , usq.question_num
from user_set_question usq
   , question q
where usq.question_id = q.id
  and usq.user_set_id = """+escape(user_set_id)+""" 
order by usq.question_num 
""").getresult()
for row in setResults:
  answered_correctly = row[0]
  days = row[1]
  hours = row[2]
  mins = row[3]
  secs = row[4]
  answer = row[5]
  answer2 = row[6]
  answer3 = row[7]
  answer4 = row[8]
  correct_answer = row[9]
  correct_answer2 = row[10]
  correct_answer3 = row[11]
  correct_answer4 = row[12]
  question_text = row[13]
  question_num = str(row[14])

  # Setup the answer display
  if not answer: answer = ""
  if not answer2: answer2 = ""  
  if not answer3: answer3 = ""  
  if not answer4: answer4 = ""  
  answer_html = answer
  if answer2: answer_html += " "+answer2
  if answer3: answer_html += " "+answer3
  if answer4: answer_html += " "+answer4
  if not answered_correctly == 't':
    answer_html = "<font color='red'>"+answer_html+"</font> "
    answer_html += "("+correct_answer
    if correct_answer2: answer_html += " "+correct_answer2
    if correct_answer3: answer_html += " "+correct_answer3
    if correct_answer4: answer_html += " "+correct_answer4
    answer_html += ")"

  html += "<tr>"
  html += "<td>"+question_num+"</td>"
  html += "<td>"+question_text+"</td>"
  html += "<td>"+answer_html+"</td>"
  html += "<td>"+formatIntervalShort(days, hours, mins, secs)+"</td>"
  html += "</tr>\n"

html += "</table></td></tr></table>"

# ----- Output ------
print navHeader()
print html
print navFooter()

