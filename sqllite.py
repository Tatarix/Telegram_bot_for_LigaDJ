import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, name TEXT, age TEXT, dj_name TEXT, id_vk TEXT, id_inst TEXT,gender TEXT, city TEXT, linc_mix TEXT, linc_logo TEXT)")
    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, '', '', '', '', '', '', '', '', ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE PROFILE SET name == '{}', age == '{}', dj_name == '{}', id_vk == '{}', id_inst == '{}', gender == '{}', city == '{}', linc_mix == '{}', linc_logo == '{}' WHERE user_id == '{}'".format(
             data['name'], data['age'], data['dj_name'], data['id_vk'], data['id_inst'],
            data['gender'], data['city'], data['linc_mix'], data['linc_logo'], user_id
        ))
        db.commit()
