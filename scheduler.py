import os

import dotenv

from crontab import CronTab

dotenv.load_dotenv()
my_cron = CronTab(user=os.getenv('user'))
for job in my_cron:
    print(job)
job = my_cron.new(command= os.getenv('python_location')+" "+os.getenv('file_location'))
job.hour.every(1)
my_cron.write()
