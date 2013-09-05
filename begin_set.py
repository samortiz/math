#!/usr/bin/env python
import pg, cgi, sys, random
import auth_session
from db_functions import *
from cgi_functions import *
from navigation import *


print "Content-type: text/html\n"
html = ""
feedbackHtml = ""

# -------- Create the Question Set ------------

# Generate a set of questions
question_type_id = getParam("question_type_id")
# validate the question_type_id
try:
  question_type_id = str(int(question_type_id))
except: 
  print "<html><body><font color='red'>Error! Invalid question_type_id specified! question_type_id="+question_type_id+"</font></body></html>"
  sys.exit(0)

row = dbGetRow("select name, level, expected_time, expected_num_questions from question_type where id='"+question_type_id+"'")
question_type_name = row[0]
question_type_level = row[1]
expected_time = row[2]
num_questions = str(row[3]) #int

# Create a new user set
user_id = auth_session.session.getUserId()
user_set_id = dbGetOne("select nextval('user_set_id_seq')")
db.query("insert into user_set (id, user_id, question_type_id, num_questions) values "+
         "('"+user_set_id+"', '"+escape(user_id)+"', '"+escape(question_type_id)+"', '"+escape(num_questions)+"') ")
allQuestionIds = dbGetCol("select question_id from question_type_question where question_type_id="+question_type_id)
questionIds = [] 

for question_num in range(1, int(num_questions)+1):

  # Find a unique question (one not already used in this set)
  counter = 0
  iInList = True
  while iInList:
    i = random.randint(0, len(allQuestionIds)-1)
    qid = allQuestionIds[i]
    iInList = (qid in questionIds)
    counter += 1
    # Give up after enough tries, unless it's the same as the previous question or two (then try again anyway!)
    if counter > 100 and (len(questionIds) > 2) and (questionIds[len(questionIds)-1] != qid) and (questionIds[len(questionIds)-2] != qid) : 
      iInList = False  # Enough trying to find a unique question, give up and dupe it!
  questionIds.append(qid)
  question_id = str(qid)
  

  # Store the question in the current user_set_question
  user_set_question_id = dbGetOne("select nextval('user_set_question_id_seq')")
  db.query("insert into user_set_question (id, user_set_id, question_id, question_num) values "+
           "('"+escape(user_set_question_id)+"', '"+escape(user_set_id)+"','"+escape(question_id)+"','"+str(question_num)+"')")



# --------- Display -----------
html += "<table class='box' style='margin-top:10px'>"
html += "<tr><td align='center'><b>"+question_type_name+" level "+question_type_level+"</b></td></tr>"
html += "<tr><td>To pass this level you need to finish in under "+expected_time+"</td></tr>"
html += "<tr><td>There are "+num_questions+" questions in this set.</td></tr>"
html += "<tr><td>Click Begin below to start your timer and begin answering questions!</td></tr>"
html += "<tr><td align='center' style='padding:10px'><a href='answer_question.py?user_set_id="+user_set_id+"&question_num=1&first_page=true' "
html += " style='border:2px solid black; padding:4px; color:black; text-decoration:none; background-color:#AAFFAA' ><b>Begin</b></a></td></tr>"
html += "</table>"

# ----- Output ------
print navHeader()
print html
print navFooter()

