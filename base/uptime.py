import requests
import psycopg2
from telegram import pagespeed
from dynaconf import settings
import numpy as np

class Base:

    conn = psycopg2.connect(dbname=settings.DBNAME,
                            user=settings.DBUSER,
                            host=settings.DBHOST,
                            password=settings.DBPASS)

    cur = conn.cursor()

    def base_marker(self, num):
        Base.cur.execute(f'select * from mystream2 WHERE num = {num}')
        query = Base.cur.fetchall()[0]
        return dict(id=query[0], author=query[1], site=query[2], status=query[3], time=query[4], error=query[5])


    def change_status(self, num, status):
        query = Base.cur.execute(f'UPDATE mystream2 SET status = {status} WHERE num = {num};')
        Base.conn.commit()
        return query

    def set_error(self, num, error, status):
        Base().cur.execute(f'UPDATE mystream2 SET error = {error}, status = {status} WHERE num = {num};')
        # Base.cur.execute(f'UPDATE mystream2 SET status = {status} WHERE num = {num};')
        Base.conn.commit()


    def set_time(self, num, time):
        query = Base().cur.execute(f'UPDATE mystream2 SET pagespeed = {time} WHERE num = {num};')
        Base.conn.commit()
        return query

    def all_authors(self):
        Base().cur.execute('SELECT DISTINCT owner from mystream2;')
        query = Base().cur.fetchall()
        names = []
        for name in query:
            names.append(name[0])
        Base.conn.commit()
        return names

    def all_rows(self):
        Base.cur.execute('SELECT max(num) FROM mystream2;')
        q = Base.cur.fetchall()[0]
        return q

    def log(self, num, site, error):
        return print(f'least: {Base.all_rows(()) - num}| site: {site} | status: {error}')

    def checker(self):
        # ran = range(1, 425)
        ran = np.arange(2, 400)
        for num in ran:
            # print(num)
            try:
                item = Base.base_marker((), num)
                site = item.get('site')
                try:
                    r = requests.get(site)
                    status = r.status_code
                    if status == 200:
                        continue
                        # Base.log((), num=num, site=site, error=200)
                        # Base.set_error((), num=num, error=200, status=True)
                    elif status == 404:
                        Base.log((), num=num, site=site, error=404)
                        Base.set_error((), num=num, error=404, status=False)
                    else:
                        Base.log((), num=num, site=site, error=300)
                        Base.set_error((), num=num, error=300, status=False)
                except requests.exceptions.InvalidSchema:
                    Base.log((), num=num, site=site, error=700)
                    Base.set_error((), num=num, error=700, status=False)
            except requests.exceptions.SSLError:
                Base.log((), num=num, site=site, error=000)
                Base.set_error((), num=num, error=000, status=False)
            except requests.exceptions.ConnectionError:
                Base.log((), num=num, site=site, error=500)
                Base.set_error((), num=num, error=500, status=False)
            except IndexError:
                Base.log((), num=num, site=site, error='SCHEMA ERROR')
                continue

    def pagespeed(self):
        ran = range(1, Base.all_rows(()))
        for num in ran:
            try:
                item = Base.base_marker((),num)
                site = item.get('site')
                time = pagespeed.ps(site)
                if time is not None:
                    Base.set_time((), time,num)
                print(f'module: Pagespeed | least: {Base.all_rows(())-num} | site: {site} | status: {time}')
                Base.conn.commit()
            except IndexError:
                continue

# /html/body/div[2]/nav[2]/ul/li[1]/a
# /html/body/div[2]/nav[2]/ul/li[2]/a
# /html/body/div[2]/nav[3]/div/div
# /html/body/div[2]/nav[3]/div/div/a[1]


