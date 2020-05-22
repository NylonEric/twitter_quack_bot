# Twitter Quack Bot

Scrape tweets from a target account, convert the text to "quacks" and tweet the results


![Link to Twitter Examples](https://twitter.com/QuackGreen/status/1212549747606740993/photo/1)
![Link to Twitter Examples](https://twitter.com/QuackGreen/status/1212549747606740993/photo/2)
![Link to Twitter Examples](https://twitter.com/QuackGreen/status/1212549747606740993/photo/3)

## Dependencies:

* Twitterscraper tool for scraping tweets from target account:

https://pypi.org/project/twitterscraper/0.2.7/

* Pyphen tool for parsing english language text by syllable:

https://pyphen.org/

* You may need to make sure that the system library **libxml2** is installed:

https://stackoverflow.com/questions/38148460/pip-install-libxml2-failed/38148662

* Twitter API tool:

https://pypi.org/project/twython/



## Cron job instructions:
Check cron_instructions.txt to create cron job to run this script periodically. (I recommend every 5 minutes)

https://www.raspberrypi.org/documentation/linux/usage/cron.md

-Use the following command to view cron jobs:
crontab -e

-Use the following command to check the log of cron jobs
grep CRON /var/log/syslog



## Twitter Setup

You'll need to setup a developer account on Twitter to get API credentials. Here is a good guide to get the process started:

https://www.instructables.com/id/Raspberry-Pi-Twitterbot/

Twitter API link:

[developer.twitter.com/apps](https://developer.twitter.com/apps)


## Credentials Configuration

Once you obtain the API credentials from Twitter, put the values in the /auth_example.py document and change the file name to "auth.py"
