#!/usr/bin/env python
import pg, cgi, random, sys
import auth_session
from db_functions import *
from cgi_functions import *
from navigation import *


# -------------- Functions -------------------
def checkAnswer(answer, correct_answer):
  """ Returns true if the answer matches the correct answer (numerically or stringly) """
  # Compare them as strings
  if answer.strip().lower() == correct_answer.strip().lower(): 
    return True 

  # Try casting both to float and comparing them 
  # This will make all these match : '1.0' '1' '1.00' '01.0'
  retVal = False
  try:
    retVal = float(answer) == float(correct_answer)
  except:
    retVal = False
  return retVal

# ----- Begin ----

print "Content-type: text/html\n"
html = ""
feedback_html = ""

# Get some paramter info
user_set_id = getParam("user_set_id")
question_num = getParam("question_num")
num_questions = dbGetOne("select num_questions from user_set where id='"+escape(user_set_id)+"'")
first_page = getParam("first_page")

# ----------------------- Previous Page (handling the submitted answer) --------------------------

# Handle the answer submitted for the previous question
answer = getParam("answer")
answer2 = getParam("answer2")
answer3 = getParam("answer3")
answer4 = getParam("answer4")

# On the first page we haven't submitted any answers yet
if not first_page:
  # Check to see if the question has already been answered (no going back and changing it!)
  prev_answer = dbGetOne("select end_time from user_set_question where user_set_id='"+escape(user_set_id)+"' "+
                         " and question_num='"+escape(question_num)+"'")
  if prev_answer == "None":
    #Get the correct answers
    correct_answers = dbGetRow("select correct_answer, correct_answer2, correct_answer3, correct_answer4 "+
      "from question q, user_set_question usq where q.id = usq.question_id "+
      " and usq.user_set_id='"+escape(user_set_id)+"' and usq.question_num='"+escape(question_num)+"' ")

    answered_correctly = "false" 
    a1 = checkAnswer(answer, correct_answers[0])
    a2 = checkAnswer(answer2, correct_answers[1])
    a3 = checkAnswer(answer3, correct_answers[2])
    a4 = checkAnswer(answer4, correct_answers[3])
    answered_correctly = str(a1 and a2 and a3 and a4)
 
   # Store the answer
    db.query("update user_set_question set end_time=now() "+
      ", answer='"+escape(answer)+"', answered_correctly='"+answered_correctly+"' "+
      ", answer2='"+escape(answer2)+"', answer3='"+escape(answer3)+"', answer4='"+escape(answer4)+"' "+
      "where user_set_id='"+user_set_id+"' and question_num='"+question_num+"' ")
    if answered_correctly != 'True':
      feedback_html += "<font color='red'>The correct answer was "+correct_answers[0]
      if correct_answers[1]: " "+correct_answers[1] 
      if correct_answers[2]: " "+correct_answers[2]
      if correct_answers[3]: " "+correct_answers[3]
      feedback_html += "</font><br>"
  else: #prev_answer != None, there is a prev answer
    feedback_html += "<font color='red'>Question "+question_num+" has already been answered, you cannot change your answer.</font><br>"


# Check if we are done the last question (finished the set)
if int(question_num) >= int(num_questions):
  # check if all the questions were answered correctly
  num_wrong = dbGetOne("select count(*) from user_set_question where user_set_id='"+escape(user_set_id)+"' and answered_correctly != true")
  num_right = dbGetOne("select count(*) from user_set_question where user_set_id='"+escape(user_set_id)+"' and answered_correctly = true")
  question_type_id = dbGetOne("select question_type_id from user_set where id = '"+escape(user_set_id)+"'")
  expected_num_questions = dbGetOne("select expected_num_questions from question_type where id='"+escape(question_type_id)+"'")
  try :
    # No wrong answers and enough right answers
    all_correct = str((num_wrong == "0") and (int(num_right) >= int(expected_num_questions)))
  except :
    all_correct = "false"
  # We have finished the last question
  db.query("update user_set set end_time=now(), all_correct='"+all_correct+"' where id='"+escape(user_set_id)+"'")

  # Forward the user to the summary page
  print "<html><head><meta http-equiv='refresh' content='0; url=set_summary.py?user_set_id="+user_set_id+"'></head><body></body></html>"
  # Do not do anything else on this page! We're done the set
  sys.exit(0)



# -------------------- Current page (next question) ----------------

# Get the next question (the question for the current page)
if not first_page: # If this is the first page we didn't submit anything before we're still on question one
  question_num = str(int(question_num) + 1)

# Update the user_set_question and start the timer! 
db.query("update user_set_question set start_time=now() where user_set_id="+escape(user_set_id)+" and question_num='"+escape(question_num)+"'")

row = dbGetRow("select qt.name, qt.level from question_type qt, user_set us where qt.id=us.question_type_id and us.id='"+escape(user_set_id)+"'")
question_type_name = row[0]
question_type_level = row[1]

question_html = dbGetOne("select q.question_html from question q, user_set_question usq where usq.question_id=q.id "+
  " and usq.user_set_id='"+escape(user_set_id)+"' and usq.question_num='"+escape(question_num)+"' ")

# Put the input boxes into the question string
question_html = question_html.replace("~A~", "<input type='text' id='answer' name='answer' size=4 class='answer_input'>")

if question_html.find("~A2~") > 0:
  question_html = question_html.replace("~A2~", "<input type='text' id='answer2' name='answer2' size=4 class='answer_input'>")
else:
  question_html += "<input type='hidden' name='answer2' value=''>"

if question_html.find("~A3~") > 0:
  question_html = question_html.replace("~A3~", "<input type='text' id='answer3' name='answer3' size=4 class='answer_input'>")
else:
  question_html += "<input type='hidden' name='answer3' value=''>"

if question_html.find("~A4~") > 0:
  question_html = question_html.replace("~A4~", "<input type='text' id='answer4' name='answer4' size=4 class='answer_input'>")
else:
  question_html += "<input type='hidden' name='answer4' value=''>"



# ----------------- Display the page --------
html += "<table class='centered' border=0 cellspacing=0 cellpadding=0 style='padding-top:10px'><tr><td>"
html += "<div style='text-align:center; font-weight:bold'>"
html += question_type_name+" level "+question_type_level+" - Question "+question_num+" of "+num_questions+" <br>"
html += "</div>"
html += """
<form name='answer_form' method='post' action='answer_question.py'>
  <input type='hidden' name='user_set_id' value='"""+user_set_id+"""'>
  <input type='hidden' name='question_num' value='"""+question_num+"""'>
  <table class='box' border=0 cellspacing=0 cellpadding=0 width='100%'>
    <tr><td align='center'>
    <table ><tr><td style='background-color:white; border:1px solid black; padding:10px;'>
      <div class='question_box'>"""+question_html+"""</div>
    </td></tr></table>
    <input type='submit' name='Submit' value='Submit'>
  </td></tr></table>
</form>
<div style='text-align:center'>
 """+feedback_html+"""
</div>
</td></tr></table>
"""

# ----- Output the display ------
headHtml = """
 <script type="text/javascript">
   function setFocus() {
     document.getElementById("answer").focus();
   }
 </script>
"""
print navHeader("", "setFocus()", headHtml)
print html
print navFooter()

