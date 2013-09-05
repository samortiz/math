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

submittingForm = getParam("Submit")
if submittingForm:
  firstname = getParam("firstname")
  lastname = getParam("lastname")
  nickname = getParam("nickname")
  email = getParam("email")
  old_password = getParam("old_password")
  password1 = getParam("password1")
  password2 = getParam("password2")
 
  db.query("update users set firstname='"+escape(firstname)+"', lastname='"+escape(lastname)+"', "+
           "nickname='"+escape(nickname)+"', email='"+escape(email)+"'  where id="+user_id)

  # If we are updating the passwords
  if password1 or password2 or old_password:
    if not old_password:
      feedbackHtml += "<font color='red'>You must provide your old password to change your password.</font><br>"
    elif not password1 or not password2:
      feedbackHtml += "<font color='red'>You must provide your new password twice</font><br>"
    elif (password1 != password2):
      feedbackHtml += "<font color='red'>Your new passwords do not match!</font><br>"
    else:
      old_password_hash = hashPassword(old_password)
      db_password_hash = dbGetOne("select password from users where id="+user_id)
      if not (old_password_hash == db_password_hash):
        feedbackHtml += "<font color='red'>You need to enter your current password in the old password field.</font><br>"
      else:
       new_password_hash = hashPassword(password1)
       db.query("update users set password='"+escape(new_password_hash)+"' where id="+user_id)
       feedbackHtml += "<font color='green'>Updated Password</font><br>"
  
  
  feedbackHtml += "<font color='green'>Saved profile information</font><br>"



# ----------------- Display the edit form --------------------------
html += "<div style='text-align:center; font-weight:bold;'>Edit Profile (<a href='add_user.py'>Add User</a>)</div>"
html += """
<table class='box' cellpadding=2px>
 <form name='theform' method='post' action='profile.py'>
"""

row = dbGetRow("select firstname, lastname, nickname, email from users where id="+escape(user_id))
firstname = row[0]
lastname = row[1]
nickname = row[2]
email = row[3]

html += "<tr><td>First Name</td><td><input type='text' name='firstname' value='"+firstname+"'></td></tr>"
html += "<tr><td>Last Name</td><td><input type='text' name='lastname' value='"+lastname+"'></td></tr>"
html += "<tr><td>Nickname (display)</td><td><input type='text' name='nickname' value='"+nickname+"'></td></tr>"
html += "<tr><td>email</td><td><input type='text' name='email' value='"+email+"'></td></tr>"

html += "<tr><td>&nbsp;</td><td></td></tr>"
html += "<tr><td><b>Update Password</b></td><td></td></tr>"
html += "<tr><td>Old Password</td><td><input type='password' name='old_password' value=''></td></tr>"
html += "<tr><td>New Password</td><td><input type='password' name='password1' value=''></td></tr>"
html += "<tr><td>New Password (again)</td><td><input type='password' name='password2' value=''></td></tr>"

html += "<tr><td colspan='100%' align=center><input type='Submit' name='Submit' value='Submit'></td></tr>"

html += "</form>"
html += "</table>"

html += "<center>"+feedbackHtml+"</center>"


# ----- Output ------
print navHeader("profile")
print html
print navFooter()

