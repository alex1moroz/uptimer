from base.check import Data

def export():
    owners = Data.owners(())
    info = []
    for owner in owners:
        if len(Data.site_error((), owner)) == 0:
            continue
        else:
            sites = f'{owner}\n' + '\n'.join(map(str, Data.site_error((), owner)))
            info.append(sites)
    if info is None:
        return "Все сайты в порядке"
    else:

        return '\n'.join(map(str, info))

def owners():
    info = Data.owners(())
    owners = '\n'.join(map(str, info))
    return f'Владельцы сатов\n{owners}'


def send_log(message):
    info = {
        "usr_id": str(message.from_user.id),
        "tag": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "text": message.text
    }
    return info
