from base.uptime import Base

print('Запуск процесса')
Base.checker(())
# print(Base.all_rows(()))
print('Процесс завершен')
Base.cur.close()
Base.conn.close()
print('Закрыли курсор')
