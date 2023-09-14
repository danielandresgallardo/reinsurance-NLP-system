import rn_crawler
import db_connector
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta

#for testing purposes
db_connector.delete_all_data()

# datetime object containing current date and time
now = datetime.utcnow().replace(tzinfo=pytz.utc)

#get last date of article on database
last_date = db_connector.fetch_last_date()
if last_date != None:
    last_date = datetime.strptime(str(last_date), '%Y-%m-%dT%H:%M:%S%z')
else:
    last_date = now - relativedelta(years=1)
    #date_temp = "2023-09-10T15:43:00+0100"
    #last_date = datetime.strptime(date_temp, '%Y-%m-%dT%H:%M:%S%z')
print(last_date)

#delete articles that are over a year old from database
db_connector.delete_old_articles(now - relativedelta(years=1))

#gr_crawler2.update_news(last_date)
rn_crawler.update_news(last_date)