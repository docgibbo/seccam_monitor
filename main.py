#This file is part of SecurityCamMonitor.

#SecurityCamMonitor is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#SecurityCamMonitor is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with SecurityCamMonitor.  If not, see <http://www.gnu.org/licenses/>.

import platform
import subprocess
from telegram.ext import Updater
import telegram
import json
import time
import sys
import traceback
import datetime

TOKEN = "5316502881:AAFTMEyDZaJkadeMqnharVoB5FvD6ZmjyEE"
CHAT_ID = "-1001789492708"
updater = Updater(token=TOKEN)
time_sleep = 900


def ping(host):
    res = False
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        c_out = subprocess.run(command, capture_output=True)
        res = c_out.stdout.decode("utf-8").lower().find("destination host unreachable") == -1
    except Exception as e:
        print(e)
        traceback.print_exc()
        updater.bot.send_message(chat_id=CHAT_ID, text="<b>Error on ping of " + host + "</b>",
                                 parse_mode=telegram.ParseMode.HTML)
    return res


try:
    #input: argv[1] = file di input, argv[2] = sleep time in sec
    if len(sys.argv) > 2 and sys.argv[2] != "":
        time_sleep = int(sys.argv[2])
    f = open(sys.argv[1])
    data = json.load(f)
    f.close()

    while True:
        now = datetime.datetime.now()
        if now.hour == 10 and (35 <= now.minute <= 50):
            updater.bot.send_message(chat_id=CHAT_ID, text="<b>Execute daily scan</b>",
                                     parse_mode=telegram.ParseMode.HTML)
        for v in data['videocams']:
            found = ping(v['ip'])
            if not found:
                updater.bot.send_message(chat_id=CHAT_ID, text="<b>Error on " + v['name'] + "</b>: no ping of " + v['ip'],
                                         parse_mode=telegram.ParseMode.HTML)
        time.sleep(time_sleep)
    updater.bot.send_message(chat_id=CHAT_ID, text="<b>CRITICAL</b>: Service Terminated",
                             parse_mode=telegram.ParseMode.HTML)
except Exception as e:
    print(e)
    traceback.print_exc()
    updater.bot.send_message(chat_id=CHAT_ID, text="<b>CRITICAL</b>: Service Terminated with error",
                             parse_mode=telegram.ParseMode.HTML)
