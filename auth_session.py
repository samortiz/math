#!/usr/bin/env python
import cookiesession, sys
session = cookiesession.CookieSession()

if not session.isLoggedIn():
  print "Content-type: text/html\n"

  # Maybe forward them to the login page?
  #<head><meta http-equiv='refresh' content='0; url=login.py'></head>\n"

  print """
<html>
<head>
<link rel=StyleSheet href="math_style.css" type="text/css">
<script type="text/javascript">
  function setFocus() {
    document.getElementById('username').focus();
  }
</script>
</head>

<body onLoad="setFocus()">

 <table class='centered' border=0 cellspacing=0 cellpadding=0><tr><td align=center>
   <font color='red'>You need to log in to access that page!</font><br>
   <br>

<!-- Cut and paste from login.py -->
<form name='theform' method='post' action='login.py'>
 <table class='box' border=0 cellspacing=0 cellpadding=2>
  <tr><td>User Name</td><td><input type='text' id='username' name='username' value='' size=15 ></td></tr>
  <tr><td>Password</td><td><input type='password' id='password' name='password' value='' size=15 ></td></tr>
  <tr><td colspan=100% align=center><input type='submit' name='submit' value='Login'></td></tr>
 </table>
</form><br>

</body>
</html>
""" 
  # Do not process anything further
  sys.exit(0)

