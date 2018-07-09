import pymongo

Sina = pymongo.MongoClient('192.168.200.47', 27017)['Sina']['Information']


def query(name):
    cursor = Sina.find({'NickName': {'$regex': name}})
    if cursor.count() > 0:
        for doc in cursor:
            print(doc)
    else:
        print('未找到相应人物')


if __name__ =='__main__':
    query('范冰冰')
