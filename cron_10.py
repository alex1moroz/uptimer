from uptime import Base


print('Запуск процесса')
Base.checker(())

print('Процесс завершен')
Base.conn.commit()
Base.cur.close()
Base.conn.close()
print('Закрыли курсор')
