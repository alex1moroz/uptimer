import tg
import cron_10
import schedule
import threading


cron = schedule.every(10).minutes.do(cron_10.cron())
telegram = tg.bot.polling(none_stop=True, interval=0)

thread1 = threading.Thread(target=telegram)
thread2 = threading.Thread(target=cron)

thread1.start()
thread2.start()

thread1.join()
thread2.join()