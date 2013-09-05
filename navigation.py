import auth_session

def navHeader(currentPage="", onLoad="", headHtml=""):
  "currentPage should be the page name without the .py on it, if it's a nav tab it will highlight it as selected"
  html = """
<html>
 <head>
  <link rel=StyleSheet href="math_style.css" type="text/css">
"""+headHtml+"""
 </head>
 <body onLoad='"""+onLoad+"""'>
<ul class="nav_bar">
 <li class="nav_tab"><a class='"""+("selected_tab" if currentPage=="home" else "nav")+"""' href="home.py">Home</a></li>
<!-- <li class="nav_tab"><a class='"""+("selected_tab" if currentPage=="history" else "nav")+"""' href="history.py">History</a></li> -->
 <li class="nav_tab"><a class='"""+("selected_tab" if currentPage=="highscores" else "nav")+"""' href="highscores.py">High Scores</a></li>
 <li class="nav_tab"><a class='"""+("selected_tab" if currentPage=="profile" else "nav")+"""' href="profile.py">Profile</a></li>
 <span style='padding-left:10px'> Welcome """+auth_session.session.getDisplayName()+""" </span>
 <li class="nav_tab" style='float:right'><a class="nav" href="logout.py">Logout</a></li>
</ul>
<div class='tab_bar_bottom'></div>
<!---- Begin Page Content -->
"""
  return html


def navFooter():
  html = """
<!----- End Page Content, Begin footer --->
<br>
</body>
</html>
"""
  return html
