import sqlite3


def add_point(uid, group_id, name,mode):
    init()
    conn = sqlite3.connect("puzzle.sqlite")
    cursor = conn.cursor()
    sql = f"select * from sign_in where uid={uid} and belonging_group={group_id} and mode = {mode}"
    data = cursor.execute(sql).fetchall()
    if data:
        point_now = data[0][1]+1
        sql = f'''UPDATE sign_in set points = {point_now} where uid = {uid} and belonging_group = {group_id} and mode = {mode}'''
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()
    else:
        sql = f'''INSERT INTO sign_in VALUES(null, {1}, {group_id}, {uid}, "{name}", "{mode}")'''
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()

def get_point(group: int, uid: int, mode: int) -> int:
    init()
    conn = sqlite3.connect("puzzle.sqlite")
    cursor = conn.cursor()
    sql = f'''select * from sign_in where belonging_group={group} and uid={uid} and mode = "{mode}"'''
    cursor.execute(sql)
    point = int(cursor.fetchone()[1])
    cursor.close()
    conn.commit()
    conn.close()
    return point



def init():
    conn = sqlite3.connect("puzzle.sqlite")
    cursor = conn.cursor()
    sql = """create table if not exists sign_in(
        id integer primary key autoincrement,
        points int not null,
        belonging_group int not null,
        uid int not null,
        sender char not null,
        mode int not null
    )
    """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def get_rank(group_id,mode):
    init()
    conn = sqlite3.connect("puzzle.sqlite")
    cursor = conn.cursor()
    order_sql = "SELECT * FROM sign_in ORDER BY points"
    data = cursor.execute(order_sql).fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    rank_text =f'本群{(mode*mode)-1}puzzle积分排名：\n获取方式：还原puzle\n-------------\n'
    rank_num = 1
    for i in data:
        if i[2]==group_id and i[-1]==mode:
            rank_text += f"{rank_num}.{i[4]}     {i[1]}\n"
            rank_num+=1
    print(rank_num)
    return rank_text



if __name__ == '__main__':
    add_point(29999,2022202,'feng',4)
    print(get_rank(2022202,4))