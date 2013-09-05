import hashlib, time, Cookie, os, datetime
from db_functions import *

class CookieSession(object):

  def __init__(self):
    self.cookie = Cookie.SimpleCookie()
    cookie_string = os.environ.get('HTTP_COOKIE', '')
    self.cookie.load(cookie_string)
   
    # Set the math_session_key
    math_session_key = ''
    if self.cookie.get('math_session_key'):
      math_session_key = self.cookie['math_session_key'].value
      # lookup the session data from the db (sessions expire a day after login)
      row = dbGetRow("select id, user_id from user_session where cookie_sid='"+escape(math_session_key)+
                        "' and logged_in and last_seen_time > now() - interval '1 day'")
      userid = ''
      db_session_id = ''
      if row:
        db_session_id = str(row[0])
        userid = str(row[1])
      if userid and db_session_id:
        row = dbGetRow("select username, firstname, lastname, nickname from users where id="+userid)
        self.userid = userid
        self.username = row[0]
        self.firstname = row[1]
        self.lastname = row[2]
        self.nickname = row[3]
        db.query("update user_session set last_seen_time=now() where id="+db_session_id)
      else:
        math_session_key = '' #invalid math_session_key (not found in db) so you're not logged in

    # If no valid math_session_key was found we will generate one
    if not math_session_key:
      # Generate a math_session_key as a hash of the current timestamp (not the best security, pretty easy to guess)
      math_session_key = hashlib.sha256(repr(time.time())+"salty").hexdigest()
      self.username = ''
      self.userid = ''
      self.firstname = ''
      self.lastname = ''
      self.nickname = ''
    
    # setup the cookie
    self.cookie.clear()
    self.cookie['math_session_key'] = math_session_key
    self.cookie['math_session_key']['domain'] = "alwaysrejoice.com"
    self.cookie['math_session_key']['path'] = "/math"
    expiration = datetime.datetime.now() + datetime.timedelta(days=1)
    self.cookie['math_session_key']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST") 


  def login(self, username):
    row = dbGetRow("select id, firstname, lastname, nickname from users where username='"+escape(username)+"'")
    self.userid = str(row[0])
    self.username = username
    self.firstname = row[1]
    self.lastname = row[2]
    self.nickname = row[3]
    db.query("update user_session set logged_in=false where logged_in and cookie_sid='"+escape(self.cookie['math_session_key'].value)+"'")
    db.query("insert into user_session (user_id, cookie_sid, logged_in) values "+
             "('"+escape(self.userid)+"', '"+escape(self.cookie['math_session_key'].value)+"', true)")

  # Used to store the cookie on the client browser
  def printCookie(self):
    print self.cookie.output()


  def logout(self):
    if self.userid != '':
      self.userid = ''
      self.username = ''
      self.firstname = ''
      self.lastname = ''
      self.nickname = ''
      db.query("update user_session set logged_in=false where cookie_sid='"+escape(self.cookie['math_session_key'].value)+"'")

  def isLoggedIn(self):
    return self.userid != ''

  def getDisplayName(self):
    return self.firstname

  def getUserId(self):
    return self.userid
