#!/usr/bin/env python
import pg, cgi
from db_functions import *
from cgi_functions import *
from misc_functions import *
import cookiesession

cookieHtml = ""
headHtml = ""
html = ""

# ---- Get the parameters -----
username = getParam("username")
password = getParam("password")


# -------- Draw the login stuff -------
html += """
<form name='theform' method='post' action='login.py'>
 <table border=0 cellspacing=0 cellpadding=2 class='box'>
  <tr><td>User Name</td><td><input type='text' id='username' name='username' value='"""+username+"""' size=15 ></td></tr>
  <tr><td>Password</td><td><input type='password' id='password' name='password' value='' size=15 ></td></tr>
  <tr><td align='center' colspan='100%'><input type='submit' name='submit' value='Login'></td></tr>
 </table>
</form>
"""

# ---- Authenticate the login ------------

# Verify the login credentials (if they exist)
if username or password:
  db_pwd = dbGetOne("select password from users where username='"+escape(username)+"'")
  password_hash = hashPassword(password) 
  if db_pwd == password_hash:
    # Successful login! -Setup the session 
    session = cookiesession.CookieSession()
    session.login(username) # log the user in
    cookieHtml = session.printCookie() # Store the cookie in the client browser
    # Redirect the user to the main page
    headHtml = "<meta http-equiv='refresh' content='0; url=home.py'>"
    html = "" #Don't show anything further, we're redirecting anyway!

  # else dbpwd != password (wrong password!)
  else: #prepend an error message
    html += "<center><font color='red'>Wrong Username/Password!</font></center>"


# -------- Output ------------
if cookieHtml:
  print cookieHtml+"\n"

print "Content-type: text/html\n"
print "<html>\n"

focusId = "username"
if username: focusId = "password"
print """<head>
 <script type="text/javascript">
   function setFocus() {
     document.getElementById('"""+focusId+"""').focus();
   }
 </script>
<link rel=StyleSheet href="math_style.css" type="text/css">
"""
if headHtml:
  print headHtml
print "</head>"

if html:
  print "<body onLoad='setFocus()'>"
  print "<center><b>Always Rejoice - Math</b></center>"
  print html
  print "</body>\n"

print "</html>\n"
