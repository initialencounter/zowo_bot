import sqlite3
def get_point(group: int, uid: int) -> int:
    conn = sqlite3.connect("cube.sqlite")
    cursor = conn.cursor()
    sql = f"select * from sign_in where belonging_group={group} and uid={uid}"
    cursor.execute(sql)
    point = int(cursor.fetchone()[1])
    cursor.close()
    conn.commit()
    conn.close()
    print(point)
# get_point(640849419, 2935116344)

def update_point(group: int, uid: int, point: int,name: str):
    conn = sqlite3.connect("cube.sqlite")
    cursor = conn.cursor()
    sql = f'''INSERT INTO sign_in VALUES(null, {point}, {group}, {uid}, "{name}")'''
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()

update_point(group=640849419, uid=2935116344,point=14, name='HoSeCoin')
get_point(640849419, 2935116344)
