from uptime import Base
from threading import Thread

def even_or_odd(num):
    if num % 2 == 0:
        result = 2
    else:
        result = 1
    return result


print('Module <<Pagespeed>> START')

all = Base.all_rows(())

def multi():
    if even_or_odd(all) == 1:
        data = all + 1
        first_1 = 1
        second_1 = data / 2
        first_2 =  second_1 + 1
        second_2 = data - 1
    else:
        first_1 = 1
        second_1 = all / 2
        first_2 = second_1 + 1
        second_2 = all
    return {'first':{'start': round(first_1), 'end': round(second_1)}, 'second':{'start': round(first_2), 'end': round(second_2)}}

print(multi())


base1 = Base.pagespeed((), start=multi()['first']['start'], end=multi()['first']['end'])
base2 = Base.pagespeed((), start=multi()['second']['start'], end=multi()['second']['end'])

thread1 = Thread(target=base1)
thread2 = Thread(target=base2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

print('Module <<Pagespeed>> END')
Base.conn.commit()
Base.cur.close()
Base.conn.close()
print('Cursor Closed')