#!/usr/bin/env python
# 
#  RUN THIS FROM THE COMMAND LINE
# the command line works better for long running scripts.
#

import pg, random
from db_functions import *

def insertQuestionType(name, level, order_by, expected_time, expected_num_questions):
  question_type_id = dbGetOne("select nextval('question_type_id_seq')")
  db.query("insert into question_type (id, name, level, order_by, expected_time, expected_num_questions) values "+
    "('"+question_type_id+"','"+name+"', '"+level+"', "+order_by+", '"+expected_time+"', "+expected_num_questions+")")
  print "Created "+name+" level "+level+" question_type_id="+question_type_id+"<br>"
  return question_type_id

def insertQuestion(question_type_id, question_html, question_text, correct_answer):
  question_id = dbGetOne("select nextval('question_id_seq')")
  db.query("insert into question (id, question_html, question_text, correct_answer, correct_answer2, correct_answer3, correct_answer4) values "+
           "('"+escape(question_id)+"', '"+escape(question_html)+"', '"+escape(question_text)+"', '"+escape(correct_answer)+"', '', '', '')")
  db.query("insert into question_type_question (question_type_id, question_id) values "+
           "('"+escape(question_type_id)+"','"+escape(question_id)+"') ")
  print "  inserted qid="+question_id+":"+question_text

# -------------------------------- Addition --------------------------------------
#if False: """
question_type_id = insertQuestionType('Addition', '1', '101', '30 sec', '10')
for x in range(2,10): #2-9
  for y in range(2,10): #2-9
    question_html = str(x)+"<br>+"+str(y)+"<br><hr>~A~"
    question_text = str(x)+" + "+str(y)
    correct_answer = str(x + y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Addition', '2', '102', '45 sec', '10')
for x in range(11,100): #11-99
  for y in range(2,10): #2-9
    question_html = str(x)+"<br>+ "+str(y)+"<br><hr>~A~"
    question_text = str(x)+" + "+str(y)
    correct_answer = str(x + y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Addition', '3', '103', '1 min', '10')
for count in range(1,500):
  uniqueXY = False
  while not uniqueXY:
    x = random.randint(10,99)
    y = random.randint(10,99)
    question_html = str(x)+"<br>+"+str(y)+"<br><hr>~A~"
    # Verify the question doesn't already exist in the database
    uniqueXY = ('' == dbGetOne("select id from question where question_html='"+escape(question_html)+"'"))

  question_text = str(x)+" + "+str(y) 
  correct_answer = str(x + y)
  insertQuestion(question_type_id, question_html, question_text, correct_answer)
  


# ------------------------------- Subtraction ---------------------------
question_type_id = insertQuestionType('Subtraction', '1', '111', '30 sec', '10')
for x in range(2,10): #2-9
  for y in range(2,10): #2-9
    if (x > y): # no negative numbers
      question_html = str(x)+"<br>-"+str(y)+"<br><hr>~A~"
      question_text = str(x)+" - "+str(y)
      correct_answer = str(x - y)
      insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Subtraction', '2', '112', '45 sec', '10')
for x in range(11,100): #11-99
  for y in range(2,10): #2-9
    question_html = str(x)+"<br>- "+str(y)+"<br><hr>~A~"
    question_text = str(x)+" - "+str(y)
    correct_answer = str(x - y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Subtraction', '3', '113', '1 min', '10')
for count in range(1,500):
  validXY = False
  while not validXY:
    x = random.randint(10,99)
    y = random.randint(10,99)
    question_html = str(x)+"<br>-"+str(y)+"<br><hr>~A~"
    # Verify the question doesn't already exist in the database
    validXY = ('' == dbGetOne("select id from question where question_html='"+escape(question_html)+"'"))
  question_text = str(x)+" - "+str(y)
  correct_answer = str(x - y)
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

#"""



# ------------------------------- Multiplication -----------------------
#if False: """
question_type_id = insertQuestionType('Multiplication', '1', '201', '30 sec', '10')
for x in range(2,10): #2-9
  for y in range(2,10): #2-9
    question_html = str(x)+"<br>x"+str(y)+"<br><hr>~A~"
    question_text = str(x)+" x "+str(y)
    correct_answer = str(x * y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)


question_type_id = insertQuestionType('Multiplication', '2', '202', '1 min', '10')
for x in range(12,100): #11-99
  for y in range(3,10): #2-9
    question_html = str(x)+"<br>x "+str(y)+"<br><hr>~A~"
    question_text = str(x)+" x "+str(y)
    correct_answer = str(x * y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)    


question_type_id = insertQuestionType('Multiplication', '3', '203', '3 min', '10')
for count in range(0,500):
  uniqueXY = False
  while not uniqueXY:
    x = random.randint(12,99)
    y = random.randint(12,99)
    question_html = str(x)+"<br>x"+str(y)+"<br><hr>~A~"
    # Verify the question doesn't already exist in the database
    uniqueXY = ('' == dbGetOne("select id from question where question_html='"+escape(question_html)+"'"))

  question_text = str(x)+" x "+str(y)
  correct_answer = str(x * y)
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

#"""


# ------------------------------- Division ----------------------------------

#if False: """
question_type_id = insertQuestionType('Division', '1', '301', '30 sec', '10')
for x in range(2,10): #2-9
  for y in range(2,10): #2-9
    product = x * y
    question_html = str(product)+"<br>&divide; "+str(x)+"<br><hr>~A~"
    question_text = str(product)+" / "+str(x)
    correct_answer = str(y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Division', '2', '302', '1 min', '10')
for x in range(3, 10): 
  for y in range(11, 100):
    product = x * y
    question_html = str(product).ljust(3," ")+"<br>&divide;&nbsp;&nbsp;"+(str(x))+"<br><hr>~A~"
    question_text = str(product)+" / "+str(x)
    correct_answer = str(y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)

#"""



# ----------------------------- Base Conversion ----------------------------------

if False: """
def toHex(num):
  hexVal = hex(num)
  return hexVal[2:].upper()

question_type_id = insertQuestionType('Hex to Decimal', '1', '10001', '30 sec', '15')
for x in range(10,16): # A-F
  x_hex = toHex(x)
  question_html = x_hex+" = ~A~"
  question_text = x_hex
  correct_answer = str(x)
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Hex to Decimal', '2', '10002', '1 min', '25')
for x in range(8,16): # A-F
  x_bin = bin(x)[2:].rjust(4,'0')
  x_hex = hex(x)[2:].upper()
  x_dec_signed = abs(int(x_bin,2) - (1 << len(x_bin)))
  question_html = "F"+x_hex+" = -~A~"
  question_text = "F"+x_hex 
  correct_answer = str(x_dec_signed)
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Hex to Decimal', '3', '10003', '2 min', '10')
for x in range(2,16): #2-16
  for y in range(2,16): 
    x_hex = toHex(x)
    y_hex = toHex(y)
    question_html = x_hex + y_hex+" = ~A~"
    question_text = x_hex+y_hex
    correct_answer = str( (x*16) + y)
    insertQuestion(question_type_id, question_html, question_text, correct_answer)




question_type_id = insertQuestionType('Binary to Decimal', '1', '10011', '30 sec', '10')
for x in range(1,16): # 1-F
  x_bin = bin(x)[2:].rjust(4,'0')
  question_html = x_bin+" = ~A~"
  question_text = x_bin
  correct_answer = str(x)
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Binary to Hex', '1', '10021', '30 sec', '10')
for x in range(1,16): # 1-F
  x_bin = bin(x)[2:].rjust(4,'0')
  x_hex = hex(x)[2:]
  question_html = x_bin+" = ~A~"
  question_text = x_bin
  correct_answer = x_hex
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

"""

if False: """
question_type_id = insertQuestionType('Hex to Binary', '1', '10031', '1 min', '25')
for x in range(1,16): # 1-F
  x_bin = bin(x)[2:].rjust(4,'0')
  x_hex = hex(x)[2:]
  question_html = x_hex+" = ~A~"
  question_text = x_hex
  correct_answer = x_bin
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

question_type_id = insertQuestionType('Decimal to Binary', '1', '10041', '1 min', '25')
for x in range(1,16): # -7 to 8 (signed)
  x_bin = bin(x)[2:].rjust(4,'0')
  if x > 7: 
    x_dec = str(int(x_bin,2) - (1 << len(x_bin)))
  else:
    x_dec = str(x)
  question_html = x_dec+" = ~A~"
  question_text = x_dec 
  correct_answer = str(x_bin)
  print question_html +" = "+correct_answer
  insertQuestion(question_type_id, question_html, question_text, correct_answer)

"""


print "\nFinished generating questions"
