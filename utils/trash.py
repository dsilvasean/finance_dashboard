import datetime
now_ = datetime.datetime.now()
now_ = now_.strftime('%d-%m-%y')
with open('./update.log', 'r+') as f:
    str_ = f.readlines()[0][11:]
    if str_ == now_:
        print('not_updating')