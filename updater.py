import gr_crawler
import rn_crawler
import rfi_crawler
import DbUtilities
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta

#for testing purposes
#DbUtilities.delete_all_articles()

# datetime object containing current date and time
now = datetime.utcnow().replace(tzinfo=pytz.utc)

#delete articles that are over a year old from database
DbUtilities.delete_old_articles(now - relativedelta(years=1))

#get last date of article on database
last_date = DbUtilities.fetch_last_date()
if last_date != None:
    last_date = datetime.strptime(str(last_date), '%Y-%m-%dT%H:%M:%S%z')
else:
    #Set last date to 1 year ago, for testing purposes just set it to 1 month ago
    #last_date = now - relativedelta(years=1)
    last_date = now - relativedelta(months=1)
print(last_date)

gr_crawler.update_news(last_date)
rn_crawler.update_news(last_date)
rfi_crawler.update_news(last_date)