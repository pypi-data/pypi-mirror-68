# coding:utf-8


def write_data(filename, data):
    if isinstance(data, str):
        with open(filename, 'a') as f:
            f.write(data + '\n')
        f.close()
    else:
        pass


def deal_data(filename):
    try:
        with open(filename, 'r+') as f:
            f.truncate()
        f.close()
    except:
        pass


