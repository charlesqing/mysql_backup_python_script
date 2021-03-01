import requests
import json
import os
import datetime

if not os.path.exists('db_backup'):
    os.mkdir('db_backup')
os.chdir('db_backup')

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=5)

today_file_name = "/mysql_backup/db_backup/cdh_db"+str(today)+".sql.zst"
yesterday_file_name = "/mysql_backup/db_backup/cdh_db"+str(yesterday)+".sql.zst"

response_code = os.system("/usr/local/mysql/bin/mysqldump -uroot -ppassword -A --single-transaction --master-data=2 | /usr/local/bin/zstd --fast=10 -1 -o cdh_db`date +%Y-%m-%d`.sql.zst")

file_size = int(os.path.getsize(today_file_name))/1024/1024

if response_code == 0:
    #text = "#### Message:\n\n > - Host MySQL Backup Completed!\n\n > - SQL_file_size:"+str(round(file_size,4))+"MB"
    text = ""
    if os.path.exists(yesterday_file_name):
        os.remove(yesterday_file_name)
else:
    text = "#### Message:\n\n > - Host MySQL Backup Error!\n\n > - Please check the server program."

dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=钉钉群的token值" 
headers = {"Content-Type": "application/json; charset=utf-8"}

post_data = {
    "msgtype": "markdown",
     "markdown": {
     "title":"Host MySQL Backup Message",
     "text":text
     }
}

requests.post(dingding_url, headers=headers, data=json.dumps(post_data))
