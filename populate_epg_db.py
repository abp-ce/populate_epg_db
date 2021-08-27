import cx_Oracle
import os
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET


def populate_epg_db(cursor, f_name):
    db = cursor
    cinsval, pinsval = [], []
    ccnt, pcnt = 0, 0
    flag = True
    for event, elem in ET.iterparse(f_name, events=("start","end")):
        if elem.tag == "channel" and event == "end":
            ch_id = disp_name = icon = None
            ch_id = elem.attrib['id']
            for c in elem:
                if c.tag == 'display-name':
                    disp_name = c.text
                elif c.tag == 'icon':
                    icon = c.attrib['src']
            cinsval.append((ch_id, disp_name, disp_name.lower(), icon))
            ccnt += 1
            if ccnt == 1500:
                db.executemany(
                    'INSERT INTO channel (ch_id, disp_name, disp_name_l, icon) VALUES (:1, :2, :3, :4)',
                    cinsval
                )
                cinsval.clear()
                ccnt = 0
            elem.clear()
        if elem.tag == "programme" and event == "end":
            if flag:
                db.executemany(
                    'INSERT INTO channel (ch_id, disp_name, disp_name_l, icon) VALUES (:1, :2, :3, :4)',
                    cinsval
                )
                flag = False
            channel = pstart = pstop = title = pdesc = cat = None
            channel = elem.attrib['channel']
            st = elem.attrib['start']
            pstart = datetime(int(st[:4]),int(st[4:6]),int(st[6:8]),int(st[8:10]),int(st[10:12]),int(st[12:14]))
            pstart -= timedelta(hours=int(st[14:18]), minutes=int(st[18:]))
            st = elem.attrib['stop']
            pstop = datetime(int(st[:4]),int(st[4:6]),int(st[6:8]),int(st[8:10]),int(st[10:12]),int(st[12:14]))
            pstop -= timedelta(hours=int(st[14:18]), minutes=int(st[18:]))
            for c in elem :
                if c.tag == 'title':
                    title = c.text
                elif c.tag == 'desc':
                    pdesc = c.text
                elif c.tag == 'category':
                    cat = c.text
            pinsval.append((channel, pstart, pstop, title, pdesc, cat))
            pcnt += 1
            if (pcnt == 1500):
                db.executemany(
                    'INSERT INTO programme (channel, pstart, pstop, title, pdesc, cat) VALUES (:1, :2, :3, :4, :5, :6)',
                    pinsval
                )
                pinsval.clear()
                pcnt=0
            elem.clear()
    db.executemany(
        'INSERT INTO programme (channel, pstart, pstop, title, pdesc, cat) VALUES (:1, :2, :3, :4, :5, :6)',
        pinsval
    )

f_name = 'xmltv.xml'
urlretrieve('https://www.teleguide.info/download/new3/xmltv.xml.gz', f_name + '.gz')

if os.path.exists(f_name):
    os.remove(f_name)
os.system('gunzip ' + f_name + '.gz')

connection = cx_Oracle.connect(user=os.getenv('ATP_USER'), password=os.getenv('ATP_PASSWORD'), dsn=os.getenv('ATP_DSN'))
cursor = connection.cursor()
cursor.execute("TRUNCATE TABLE programme")
cursor.execute("TRUNCATE TABLE channel")
populate_epg_db(cursor, f_name)

connection.commit()  # uncomment to make data persistent
print("EPG was successfully populated")

# Now query the rows back
#for row in cursor.execute('select * from channel'):
    #print(row)

