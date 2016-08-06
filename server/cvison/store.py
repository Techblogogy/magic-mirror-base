from dbase.dbase import dbase as db
from api_cal.weather import Weather

from minfo import app_dir

import random, json
import requests

TAG_LIMIT = 5

class clothes:

    # self.d_codes = ["business-casual", "casual", "formal", "sportswear"]

    @classmethod
    def setup(self):
        # Main Clothes Storage Table
        db.qry("""
            CREATE TABLE IF NOT EXISTS clothes (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                thumbnail TEXT NOT NULL,
                dresscode TEXT NOT NULL,
                t_wears INT NOT NULL DEFAULT 0,
                liked INT NOT NULL DEFAULT 0,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Clothes tags table
        db.qry("""
            CREATE TABLE IF NOT EXISTS clothes_tags (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                c_id INTEGER NOT NULL,

                tag TEXT NOT NULL
            )
        """)

        # Clothes Metadata Table (add value when item is worn)
        db.qry("""
            CREATE TABLE IF NOT EXISTS clothes_meta (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                c_id INTEGER NOT NULL,

                temperature INT NOT NULL,
                t_time TEXT
            )
        """)

    # Add clothing item
    @classmethod
    def add(self, dresscode, thumbnail, name=None):
        url = "http://93.73.73.40:8000/"
        file = {'file': open(app_dir+'/'+thumbnail, 'rb')}

        r = requests.post(url, files=file)
        cnt = json.loads(r.content)

        print cnt['dress']

        db.qry(
            "INSERT INTO clothes(name, thumbnail, dresscode) VALUES (?, ?, ?)",
            (name, thumbnail, cnt['dress'], )
        )

        return db.qry("SELECT * FROM clothes WHERE id=?", (db.last_id(), ) )

    # Add Tags to items
    @classmethod
    def add_tags(self, c_id, tags):
        # db.qry("DELETE FROM clothes_tags WHERE c_id=?", (c_id,))
        # return "[]"

        count = db.qry("""
            SELECT COUNT(*) as cnt
            FROM clothes_tags
            WHERE c_id=?
        """, (c_id,))[0]["cnt"]

        print "[TB count]: %d" % (count)

        if count > TAG_LIMIT:
            return "[]"

        a_tags = tags.strip().split(",")
        a_list = []



        print a_list

        if count == 0:
            for a_tag in a_tags:
                a_list.append( (c_id, a_tag,) )

            db.qry_many("""
                INSERT INTO clothes_tags(c_id, tag)
                VALUES (?,?)
            """, a_list)
        else:
            for a_tag in a_tags:
                a_list.append( (c_id, a_tag, a_tag) )

            db.qry_many("""
                INSERT INTO clothes_tags(c_id, tag)
                SELECT ?,?
                WHERE NOT EXISTS(SELECT tag FROM clothes_tags WHERE tag=?)
            """, a_list)

        return db.qry("SELECT * FROM clothes_tags WHERE c_id=?", (c_id,))

    # TODO: Remove tags from items
    @classmethod
    def rmv_tags(self, id):
        pass

    # TODO: Returns page count
    @classmethod
    def pages(self):
        pass

    # Returns video id
    @classmethod
    def get_video(self, id):
        print "[DEBUG] id is: %s" % (id)
        path = db.qry("SELECT thumbnail FROM clothes WHERE id=?", (id,))[0]['thumbnail']
        path = path.split(".")

        return path[0] + ".mp4"

    @classmethod
    def get_smart(self, query, lim, ofs):
        d_codes = ["business-casual", "casual", "formal", "sportswear"]

        # Create indexes to speed up perfomance
        db.qry("CREATE INDEX IF NOT EXISTS code_dx ON clothes(dresscode)")
        db.qry("CREATE INDEX IF NOT EXISTS wears_dx ON clothes(t_wears)")

        db.qry("CREATE INDEX IF NOT EXISTS tag_dx ON clothes_tags(tag)")

        db.qry("CREATE INDEX IF NOT EXISTS id_meta_dx ON clothes_meta(c_id)")
        db.qry("CREATE INDEX IF NOT EXISTS id_tags_dx ON clothes_tags(c_id)")
        # return db.qry("SELECT * FROM sqlite_master WHERE type = 'index';")

        base_qry = """
            SELECT
                *,
                (SELECT group_concat(tag, ', ') as tags
                FROM clothes_tags
                WHERE clothes_tags.c_id = clothes.id
                GROUP BY c_id) as tags
            FROM
                (SELECT
                    c_id,
                    CASE
                        WHEN temp_group(temperature) = ? THEN 2
                        WHEN temp_group(temperature) < ? THEN 1
                        ELSE 0 END as temp_rank,
                    temp_group(temperature) as temp,
                    COUNT(temp_group(temperature)) as temp_count,
                    (SELECT MAX(t_time) FROM clothes_meta WHERE clothes_meta.c_id=cm.c_id ) as last_date
                FROM clothes_meta as cm
                GROUP BY c_id, temp
                ORDER BY temp_rank DESC, temp DESC, temp_count DESC) as t_qry
                JOIN clothes ON( clothes.id=t_qry.c_id )
            WHERE deleted = 0 %s
            ORDER BY liked DESC, temp_rank DESC, temp DESC, t_wears DESC, temp_count DESC
            LIMIT ? OFFSET ?
        """

        w_rng = Weather.w_temp_range()[0]
        w_temp = db._temp_group(w_rng)

        print "[DEBUG] Current temperatue: %d" % (w_rng)
        print "[DEBUG] Temperature Range: %d" % (w_temp)

        try:
            d_codes.index(query)
            return db.qry(base_qry % ("AND dresscode=?"), (w_temp, w_temp, query, lim, ofs*lim))
        except ValueError:
            return db.qry(base_qry % ("AND tags LIKE ?"), (w_temp, w_temp, "%"+query+"%", lim, ofs*lim))
        # except:
        #     return {'error': "TOTAL ERROR"}

    # Get all items
    @classmethod
    def get_all(self):
        return db.qry("""
            SELECT
                id, thumbnail, dresscode, t_wears,
                    (SELECT group_concat(tag, ', ') as tags
                    FROM clothes_tags
                    WHERE clothes_tags.c_id = clothes.id
                    GROUP BY c_id) as tags
            FROM clothes
            WHERE deleted=0
        """)

    # Get items in range
    @classmethod
    def get(self, lim, ofs):
        return db.qry("""
            SELECT id, thumbnail, dresscode, t_wears,
                (SELECT group_concat(tag, ', ') as tags
                FROM clothes_tags
                WHERE clothes_tags.c_id = clothes.id
                GROUP BY c_id) as tags
            FROM clothes
            WHERE deleted=0 LIMIT ? OFFSET ?
        """,
            (lim, ofs*lim)
        )

    # Get page items
    def page_count(self, pp):
        all_items = db.qry("SELECT COUNT(*) as ct FROM clothes")[0]["ct"]

        return all_items/pp

    # Get item by id
    @classmethod
    def get_item(self, id):
        return db.qry("""
            SELECT
                id, thumbnail, dresscode, t_wears,
                    (SELECT group_concat(tag, ', ') as tags
                    FROM clothes_tags
                    WHERE clothes_tags.c_id = clothes.id
                    GROUP BY c_id) as tags
            FROM clothes
            WHERE deleted=0 AND id=?
        """,
            (id,)
        )

    # Mark item as worn
    @classmethod
    def worn(self, id):
        db.qry(
            "UPDATE clothes SET t_wears=t_wears+1 WHERE id=?",
            (id, )
        )
        db.qry(
            "INSERT INTO clothes_meta (c_id, temperature, t_time) VALUES (?, ?, date('now'))",
            (id, Weather.w_current_temp(), )
        )

        return ""
        # return db.qry("SELECT * FROM clothes_meta")
        # return Weather.w_current_temp()

    # Get items meta
    @classmethod
    def get_meta(self):
        return db.qry("""
            SELECT * FROM clothes_meta
        """)

    @classmethod
    def worn_tmp(self, c_id, w, dt):
        db.qry(
            "UPDATE clothes SET t_wears=t_wears+1 WHERE id=?",
            (c_id, )
        )

        db.qry(
            "INSERT INTO clothes_meta (c_id, temperature, t_time) VALUES (?, ?, ?)",
            (c_id, w, dt,)
        )

    # Like item (ID of element, Like state (0) for no, (1) for yes)
    @classmethod
    def set_like(self, id, like):
        db.qry(
            "UPDATE clothes SET liked=? WHERE id=?",
            (id, like, )
        )

    @classmethod
    def delete(self, id):
        db.qry("DELETE FROM clothes WHERE id=?", (id, ))
        db.qry("DELETE FROM clothes_meta WHERE id=?", (id, ))
        db.qry("DELETE FROM clothes_tags WHERE id=?", (id, ))

    # NOTE: Testing data fill
    @classmethod
    def fill_junk(self):
        d_codes = ["business-casual", "casual", "formal", "sportswear"]

        d_tags = ["clubwear", "meetups", "beach", "work", "time", "special", "bugs", "whatistag", "needhelp", "Tanya?", "howareyou", "surprise", "nonono", "whatelse"]

        # Clear out clothes table
        db.qry("DELETE FROM clothes")
        db.qry("VACUUM")
        db.qry("DELETE FROM sqlite_sequence WHERE name='clothes'")

        # Clear out clothes meta table
        db.qry("DELETE FROM clothes_meta")
        db.qry("VACUUM")
        db.qry("DELETE FROM sqlite_sequence WHERE name='clothes_meta'")

        # Clear out clothes tags table
        db.qry("DELETE FROM clothes_tags")
        db.qry("VACUUM")
        db.qry("DELETE FROM sqlite_sequence WHERE name='clothes_tags'")

        for i in range(1,100):
            # print random.choice(d_codes)
            self.add(random.choice(d_codes), "thum%s.jpg"%str(random.randint(1,13)))
            i_id = db.last_id()

            # Randomly add tags
            for t in range( 1, random.randint(1, len(d_tags)+1 ) ):
                self.add_tags(i_id, random.choice(d_tags) )

            # 20% chanse to set like
            if random.random() <= 0.1:
                self.set_like(1, i_id)

            # Randomly wear items
            for a in range(1,random.randint(2,40)):
                self.worn_tmp(str(i_id), str(random.randint(-15,30)), "%s-%02d-%02d"%( str(random.randint(2013,2016)), random.randint(1,8), random.randint(1,30) ) )

        return self.get_all()


clothes.setup()
# clothes.add("casual", "1.png", 20, "somthing 1", "cool, winter")
# clothes.worn(1)
# print clothes.get_all()
