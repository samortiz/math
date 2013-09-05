#!/usr/bin/env python
import cgi
# --------------- CGI Functions ------------------------

form = cgi.FieldStorage() # parse query params
def getParam(paramName):
  retVal = ""
  if form.has_key(paramName): 
    retVal = form[paramName].value
  #int verification
  #if (not re.match("[0-9]{1,4}", hnum)): hnum = ""
  return retVal

