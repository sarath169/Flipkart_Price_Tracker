from crontab import CronTab
my_cron = CronTab(user='sarath')
for job in my_cron:
    print(job)
job = my_cron.new(command=' /home/sarath/anaconda3/bin/python  /home/sarath/Documents/Flipkart_Price_Tracker/scraper.py')
job.minute.every(5)
my_cron.write()
