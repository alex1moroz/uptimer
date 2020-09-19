import psycopg2
import re
from dynaconf import settings

class Data:
    conn = psycopg2.connect(dbname=settings.DBNAME,
                            user=settings.DBUSER,
                            host=settings.DBHOST,
                            password=settings.DBPASS)
    cur = conn.cursor()

    table = 'mystream2'

    def base(self):
        Data.cur.execute(f'select * from {Data.table};')
        data = Data.cur.fetchall()
        return len(data)


    def owners(self):
        Data.cur.execute(f'SELECT DISTINCT owner from {Data.table};')
        data = Data.cur.fetchall()
        owner = []
        for num in data:
            owner.append(num[0])
        return owner


    def site_error(self, owner):
        Data.cur.execute(f"SELECT site FROM {Data.table} where status is not TRUE and owner = '{owner}'")
        data = Data.cur.fetchall()
        site = []
        for num in data:
            site.append(num[0])
        return site

    def error_data(self):

        data = []
        for owner in Data.owners():
            sites = Data.site_error(owner)
            if len(sites) == 0:
                continue
            else:
                list = dict(owner=owner, site=sites)
                data.append(list)

        return data

    def add_row(self, author, url):
        num = Data.base(()) + 1
        if re.match(r'^[a-zA-Z]*', url) == "https":
            add = Data.cur.execute(f"INSERT INTO {Data.table} VALUES ({num}, '{author}', {url});")
        else:
            add = None
        return add
