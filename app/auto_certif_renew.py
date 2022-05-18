#!/opt/conda/bin/python
'''
IF YOU USE `let's encrypt` SSL, SETUP CREDENTIALS INITIALLY, AND
KINDLY RUN THIS PYTHON SCRIPT ALONE, NO NEED TO RUN SERVERS or api_expose.py
IT WILL TAKE CARE OF SSL RENEWAL AUTOMATICALLY :) AND RESTARTING SERVERS
IT IS IMPORTANT THAT THIS SCRIPT MUST BE RUN IN PYTHON2 (not 3)
'''

from apscheduler.schedulers.background import BackgroundScheduler
import time
import datetime
import subprocess


def auto_runner():
    print(datetime.datetime.now())
    print('Clearing All exisitng PY3 Processes .#.#.#.#')
    process = subprocess.run("sudo killall python3".split(),  universal_newlines=True)
    print('Updating LetsEncrypt Certificates using `certbot` .....')
    process = subprocess.run("sudo service apache2 restart".split(),  universal_newlines=True)
    ##---
    process = subprocess.run("sudo certbot renew --force-renewal".split(),  universal_newlines=True)
    ##---
    process = subprocess.run("sudo service apache2 stop".split(),  universal_newlines=True)

    ###
    ##<<< UPDATE_AS_NEEDED
    process2 = subprocess.run("sudo env PATH=$PATH GOOGLE_APPLICATION_CREDENTIALS=/path_to_cred/a.json /opt/conda/bin/python3 api_expose.py".split() ,
                            universal_newlines=True)



if __name__ == '__main__':

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(auto_runner, 'interval', days=75, max_instances=2)
    scheduler.start()
    ## First time runner
    auto_runner()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()