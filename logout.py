#!/usr/bin/env python
import auth_session

print "Content-type: text/html\n"
html = ""

auth_session.session.logout()

html += "<table class='box'><tr><td>"
html += "You have been logged out<br>"
html += "<br>"
html += "<center><a href='login.py'>Log back in</a></center>"
html += "</td></tr></table>"

print """
<html>
<head>
  <link rel=StyleSheet href="math_style.css" type="text/css">
</head>
<body>
 """+html+"""
</body>
</html>
"""

