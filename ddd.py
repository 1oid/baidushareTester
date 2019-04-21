from baidushare.db import BaiduShareDb
from config import *

with open("insert.txt") as f:
    lines = [x.strip() for x in f.readlines()]

db = BaiduShareDb(db_server, db_user, db_pwd, db_select)
for i in lines:
    db.insert(i, 10)
