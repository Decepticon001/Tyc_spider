import pymysql


connect = pymysql.connect(
                host="47.104.73.227",
                db="headline",
                user="root",
                passwd="royasoft",
                charset='utf8',
                use_unicode=True)
cursor = connect.cursor()

cursor.execute("select Corp_Name from tyc_e_corp_cop;")

res = cursor.fetchall()
for i in res:
    # print(str(i)[2:-3])
    d = str(i)[2:-3]
    print(d)