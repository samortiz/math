#!/usr/bin/env python
import pg, cgi
import auth_session
from db_functions import *
from cgi_functions import *
from navigation import *
from misc_functions import *

print "Content-type: text/html\n"
html = ""
feedbackHtml = ""
user_id = auth_session.session.getUserId()

# ------------------- Handle the submitted form -------------------------
username = ""
firstname = ""
lastname = ""
nickname = ""
email = ""

submittingForm = getParam("Submit")
if submittingForm:
  username = getParam("username")
  firstname = getParam("firstname")
  lastname = getParam("lastname")
  nickname = getParam("nickname")
  email = getParam("email")
  password1 = getParam("password1")
  password2 = getParam("password2")

  # Check for valid fields
  if not username or not firstname or not lastname or not nickname:
    feedbackHtml += "<font color='red'>YOu must provide all the information to create a user.</font><br>"
  
  #Password check
  elif not password1 or not password2 or (password1 != password2):
    feedbackHtml += "<font color='red'>YOu must provide the same password twice.</font><br>" 
  
  else:
    # check if the username is free
    userid = dbGetOne("select id from users where username='"+escape(username)+"'")   
    if userid:
      feedbackHtml += "<font color='red'>The username "+username+" is already uesd, sorry you will have to choose a different one.</font><br>"
    else:
      # Create the user in the database
      password_hash = hashPassword(password1)
      db.query("insert into users (username, firstname, lastname, nickname, email, password) values "+
              "( '"+escape(username)+"', '"+escape(firstname)+"', '"+escape(lastname)+"', "+
              "  '"+escape(nickname)+"', '"+escape(email)+"', '"+escape(password_hash)+"' ) ")
      feedbackHtml += "<font color='green'>Created User</font><br>"
  


# ----------------- Display the edit form --------------------------
html += "<div style='text-align:center; font-weight:bold;'>Create User </div>"
html += """
<table class='box' cellpadding=2px>
 <form name='theform' method='post' action='add_user.py'>
"""
html += "<tr><td>User Name (login)</td><td><input type='text' name='username' value='"+username+"'></td></tr>"
html += "<tr><td>First Name</td><td><input type='text' name='firstname' value='"+firstname+"'></td></tr>"
html += "<tr><td>Last Name</td><td><input type='text' name='lastname' value='"+lastname+"'></td></tr>"
html += "<tr><td>Nickname (display)</td><td><input type='text' name='nickname' value='"+nickname+"'></td></tr>"
html += "<tr><td>email</td><td><input type='text' name='email' value='"+email+"'></td></tr>"
html += "<tr><td>Password</td><td><input type='password' name='password1' value=''></td></tr>"
html += "<tr><td>Password (again)</td><td><input type='password' name='password2' value=''></td></tr>"

html += "<tr><td colspan='100%' align=center><input type='Submit' name='Submit' value='Submit'></td></tr>"

html += "</form>"
html += "</table>"

html += "<center>"+feedbackHtml+"</center>"


# ----- Output ------
print navHeader("profile")
print html
print navFooter()

