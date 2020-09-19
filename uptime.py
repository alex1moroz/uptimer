import requests
import psycopg2
import json
import re
import pagespeed
from dynaconf import settings


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
        return query

    def set_error(self, num, error):
        query = Base().cur.execute(f'UPDATE mystream2 SET error = {error} WHERE num = {num};')
        return query


    def set_time(self, num, time):
        query = Base().cur.execute(f'UPDATE mystream2 SET pagespeed = {time} WHERE num = {num};')
        return query

    def all_authors(self):
        Base().cur.execute('SELECT DISTINCT owner from mystream2;')
        query = Base().cur.fetchall()
        names = []
        for name in query:
            names.append(name[0])
        return names

    def all_rows(self):
        Base.cur.execute('SELECT num FROM mystream2;')
        q = Base.cur.fetchall()
        return len(q)

    def checker(self):
        ran = range(1, Base.all_rows(()))
        for num in ran:
            item = Base.base_marker((),num)
            site = item.get('site')
            try:
                r = requests.get(site)
                status = r.status_code
                if status == 200:
                    error = 200
                    basestatus = True
                else:
                    error = 404
                    basestatus = False
            except requests.exceptions.SSLError:
                basestatus = False
                error = 000
            except requests.exceptions.ConnectionError:
                basestatus = False
                error = 500
            Base.set_error((), num, error)
            Base.change_status((), num, basestatus)

            print(f'least: {Base.all_rows(())-num   }| site: {site}| status: {error}')

    def pagespeed(self, start, end):
        ran = range(start, end)
        for num in ran:
            item = Base.base_marker((),num)
            site = item.get('site')
            time = pagespeed.ps(site)
            if time is not None:
                Base.set_time((), time,num)
                print(f'module: Pagespeed | least: {Base.all_rows(())-num} | site: {site} | status: {time}')