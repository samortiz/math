#!/usr/bin/env python
# Misc functions for math
import hashlib

def hashPassword(password):
  return hashlib.sha256(password+"salty").hexdigest()

def formatInterval(days, hours, mins, secs):
  retVal = ""
  if days:
    retVal += "%.0f day" % days
    if round(days) > 1: retVal += "s"
    retVal += " "
  if hours:
    retVal += "%.0f hour" % hours
    if round(hours) > 1: retVal += "s"
    retVal += " "
  if mins:
    retVal += "%.0f minute" % mins
    if round(mins) > 1: retVal += "s"
    retVal += " "
  if secs:
    retVal += "%.0f second" % secs
    if round(secs) > 1: retVal += "s"
  return retVal

def formatIntervalShort(days, hours, mins, secs):
  retVal = ""
  if days:
    retVal += "%.0fd" % days
    retVal += " "
  if hours:
    retVal += "%.0fh" % hours
    retVal += " "
  if mins:
    retVal += "%.0fm" % mins
    retVal += " "
  if secs:
    retVal += "%.0fs" % secs
  return retVal

