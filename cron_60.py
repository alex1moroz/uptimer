from base.uptime import Base

print('Module <<Pagespeed>> START')

all = Base.all_rows(())

Base.pagespeed(())

print('Module <<Pagespeed>> END')
Base.cur.close()
Base.conn.close()
print('Cursor Closed')