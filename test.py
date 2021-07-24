from search.config.config import Config
from search.database.mysql import Simple

db = Simple(Config.MYSQL['MYSQL_HOST'], Config.MYSQL["MYSQL_PORT"], Config.MYSQL['MYSQL_USER'],
            Config.MYSQL['MYSQL_PASSWORD'], "so")


# a = db.query_data("so_backup", "url")
# for i in a:
#     #print(i)


def test_in_database(url):
    data = db.query_data("so_backup", "url")
    for i in data:
        a = i[0]
        if url == a:
            return True
    return False


print(test_in_database("http://www.minecraftxz.com/?r=feedback%2Findex"))
