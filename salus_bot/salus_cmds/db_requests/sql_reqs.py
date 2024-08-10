import sqlite3
import os
from requests import request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# add requests

def add(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  add = 'INSERT INTO scammers(subject_id, sr_id, reporter_id, anonymous, game, tag_id, alts, reason, proofs, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
  payload = (arg['subject_id'], arg['sr_id'], arg['reporter_id'], arg['anonymous'], arg['game'], arg['tag_id'], arg['alts'], arg['reason'], arg['proofs'], arg['timestamp'])
  cur.execute(add, payload)
  con.commit()
  cur.close()
  con.close()
  return True

# search requests

def search(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search = "SELECT * FROM scammers WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}
  req = cur.execute(search, payload)
  try:
    req = req.fetchall()[0]
  except IndexError:
    return False
  if not req:
    return None
  tag = search_tag(req[1])
  result = {
    'subject_id' : req[0], 
    'tag_id' : tag['tag_id'],
    'tag_name' : tag['tag_name'],
    'tag_color' : str(tag['tag_color']),
    'sr_id' : req[2], 
    'reporter_id' : req[3],
    'anonymous' : req[4], 
    'game' : req[5],
    'alts' : req[6], 
    'reason' : req[7], 
    'proofs' : req[8], 
    'timestamp' : req[9]
  }
  con.commit()
  cur.close()
  con.close()
  return result

def check_report(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search_py = "SELECT subject_id FROM scammers WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}
  req = cur.execute(search_py, payload)
  try:
    req = req.fetchall()[0]
  except IndexError:
    con.commit()
    cur.close()
    con.close()
    return False
  con.commit()
  cur.close()
  con.close()
  return True
# delete requests

def delete(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search = "DELETE FROM scammers WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg['subject_id']}
  try:
    req = cur.execute(search, payload)
  except sqlite3.Error as err:
    con.commit()
    cur.close()
    con.close()
    return False
  con.commit()
  cur.close()
  con.close()
  return True

# reason requests

def get_reason(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search = "SELECT reason FROM scammers WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}
  req = cur.execute(search, payload)
  result = req.fetchall()[0][0]
  con.commit()
  cur.close()
  con.close()
  return result

def update_reason(arg, subject):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  update = 'UPDATE scammers SET reason = ? WHERE subject_id = ?;'
  payload = (arg, subject)
  cur.execute(update, payload)
  con.commit()
  cur.close()
  con.close()
  return True

# proofs requests

def get_proofs(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search = "SELECT proofs FROM scammers WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}
  req = cur.execute(search, payload)
  result = req.fetchall()[0][0]
  con.commit()
  cur.close()
  con.close()
  return result

def update_proofs(arg, subject):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  update = 'UPDATE scammers SET proofs = ? WHERE subject_id = ?;'
  payload = (arg, subject)
  cur.execute(update, payload)
  con.commit()
  cur.close()
  con.close()
  return True

# alts requests

def get_alts(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search = "SELECT alts FROM scammers WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}
  req = cur.execute(search, payload)
  result = req.fetchall()[0][0]
  cur.close()
  con.close()
  return result

def update_alts(arg, subject):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  update = 'UPDATE scammers SET alts = ? WHERE subject_id = ?;'
  payload = (arg, subject)
  cur.execute(update, payload)
  con.commit()
  cur.close()
  con.close()
  return True

def clear_alts(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  update = "UPDATE scammers SET alts = NULL WHERE subject_id =:subject_id;"
  payload = {'subject_id' : arg}
  cur.execute(update, payload)
  con.commit()
  cur.close()
  con.close()
  return None

# tag requests

def search_tag(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search = "SELECT * FROM tags WHERE tag_id =:tag_id"
  payload = {'tag_id' : arg}
  req = cur.execute(search, payload)
  try:
    req = req.fetchall()[0]
  except IndexError:
    return False
  if not req:
    return None
  result = {
    'tag_id' : req[0],
    'tag_name' : req[1],
    'tag_color' : int(req[2], 16)
  }
  cur.close()
  con.close()
  return result

def update_tag(arg, subject): # updates the tag of a report
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  update = 'UPDATE scammers SET tag_id = ? WHERE subject_id = ?;'
  payload = (arg, subject)
  cur.execute(update, payload)
  con.commit()
  cur.close()
  con.close()
  return True

def update_tag_color(id, arg): # updates a tag color
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  update = 'UPDATE tags SET tag_color = ? WHERE tag_id = ?;'
  payload = (id, arg)
  cur.execute(update, payload)
  con.commit()
  cur.close()
  con.close()
  return True

# sr profil requests

def sr_reports(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  sql_rq = 'SELECT subject_id FROM scammers WHERE sr_id =:sr_id'
  payload = {'sr_id' : arg}
  result = cur.execute(sql_rq, payload)
  result = result.fetchall()
  con.commit()
  cur.close()
  con.close()
  return len(result)

# old data requests

def old_search(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  search_py = "SELECT subject_id FROM old_ids WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}
  req = cur.execute(search_py, payload)
  try:
    req = req.fetchall()[0]
  except:
    con.commit()
    cur.close()
    con.close()
    return False
  con.commit()
  cur.close()
  con.close()
  return req[0]

def old_remove(arg):
  con = sqlite3.connect(os.path.join(BASE_DIR, "salus.sqlite"))
  cur = con.cursor()
  old_rm = "DELETE FROM old_ids WHERE subject_id =:subject_id"
  payload = {'subject_id' : arg}  
  cur.execute(old_rm, payload)
  con.commit()
  cur.close()
  con.close()
  return True