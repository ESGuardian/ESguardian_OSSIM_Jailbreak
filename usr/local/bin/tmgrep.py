#! /usr/bin/python
# -*- coding: cp1251 -*-
# ����� esguardian@outlook.com
# ������ 1.0.3
# ����� � ������� ��� � ������� ��������� ������ ������ 
# ���������� ������ ����� ������� tmg-web
#
import sys
import MySQLdb
import codecs
from datetime import date, timedelta
from OSSIM_helper import get_db_connection_data


# Datababe connection config.
(dbhost,dbuser,dbpass) = get_db_connection_data()
dbshema='alienvault_siem'
# --- End of Database config

# ---- Init 

period=1
if len(sys.argv) > 1:
    period=int(sys.argv[1])


today=date.today()
enddate=today.strftime('%Y:%m:%d')
endtime=enddate + ' 06:00:00' # UTC time
startdate=(today - timedelta(days=period)).strftime('%Y:%m:%d')
starttime=startdate + ' 06:00:00'

outfilename='DLP-' + today.strftime('%Y-%m-%d') + '.csv'
outfullpath='/usr/local/ossim_reports/' + outfilename

mytz="'+03:00'"
mycharset='cp1251'
dbcharset='utf8'
colheader=u'�����;��������;������������;������� URL;������� ����;������ ���� ������;��������;������ WhoIs\n'


conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpass, db=dbshema, charset=dbcharset) 
cursor = conn.cursor() 

# ---- End of Init
when = "timestamp between '" + starttime + "' and '" + endtime + "'"

# start
tabheader=u'\n\n\n������������ �������� ������ � �������� �� ������ ' + startdate + ' - ' + enddate + '\n\n'
what="convert_tz(timestamp,'+00:00'," + mytz +") as time, inet_ntoa(conv(HEX(ip_src), 16, 10)), username, userdata1, userdata2, userdata3, userdata4 from acid_event join extra_data on (acid_event.id=extra_data.event_id)"
where="acid_event.plugin_id=9004 and acid_event.plugin_sid=2000"
select="select  " + what + " where " + where + " and " + when + " order by time"
cursor.execute(select)
with codecs.open(outfullpath, 'a', encoding=mycharset) as out:
     out.write(tabheader + colheader) 
     row = cursor.fetchone() 
     while row:
         out.write(';'.join([str(c).decode(dbcharset).replace(';',',').strip() for c in row]) + '\n')
         row = cursor.fetchone()
out.close()
# --- End of All
conn.close()
