import os

import dotenv

from crontab import CronTab

dotenv.load_dotenv()
my_cron = CronTab(user=os.getenv('user'))
for job in my_cron:
    print(job)
scraper_job = my_cron.new(command= os.getenv('python_location')+" "+os.getenv('scraper_location'))
scraper_job.hour.every(1)
alert_job=my_cron.new(command= os.getenv('python_location')+" "+os.getenv('alert_location'))
alert_job.minute.every(30)
my_cron.write()
