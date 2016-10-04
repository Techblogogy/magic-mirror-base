# from dbase.dbase import dbase as db
from dbase.dataset import Dataset

# from api_cal.weather import Weather

import random, json, requests

class Clothes(Dataset):

    # self.d_codes = ["business-casual", "casual", "formal", "sportswear"]

    def create_tables(self):
        # Import constants
        self.tag_limit = self._cfg.getint("DRESS CODE", "tag_limit")
        self.site_url = self._cfg.get("DRESS CODE", "dresscode_url")

        # Main Clothes Storage Table
        self._db.qry("""
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
        self._db.qry("""
            CREATE TABLE IF NOT EXISTS clothes_tags (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                c_id INTEGER NOT NULL,

                tag TEXT NOT NULL
            )
        """)

        # Clothes Metadata Table (add value when item is worn)
        self._db.qry("""
            CREATE TABLE IF NOT EXISTS clothes_meta (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                c_id INTEGER NOT NULL,

                temperature INT NOT NULL,
                t_time TEXT
            )
        """)

    # Create indexes to speed up perfomance
    def init_tables(self):
        self._db.qry("CREATE INDEX IF NOT EXISTS code_dx ON clothes(dresscode)")
        self._db.qry("CREATE INDEX IF NOT EXISTS wears_dx ON clothes(t_wears)")

        self._db.qry("CREATE INDEX IF NOT EXISTS tag_dx ON clothes_tags(tag)")

        self._db.qry("CREATE INDEX IF NOT EXISTS id_meta_dx ON clothes_meta(c_id)")
        self._db.qry("CREATE INDEX IF NOT EXISTS id_tags_dx ON clothes_tags(c_id)")


    # Add clothing item
    def add(self, dresscode, thumbnail, name=None):
        # file = {'file': open(app_dir+'/cls/'+thumbnail, 'rb')}
        # r = requests.post(self.site_url, files=file)
        # cnt = json.loads(r.content)

        # Temporal debug option
        cnt = {'dress': [{"code":"casual"}]}

        self._log.debug(cnt['dress'])

        self._db.qry(
            "INSERT INTO clothes(name, thumbnail, dresscode) VALUES (?, ?, ?)",
            (name, thumbnail, cnt['dress'][0]['code'], )
        )

        return self._db.qry("SELECT * FROM clothes WHERE id=?", (self._db.last_id(), ) )

    # Add Tags to items
    def add_tags(self, c_id, tags):
        # self._db.qry("DELETE FROM clothes_tags WHERE c_id=?", (c_id,))
        # return "[]"

        count = self._db.qry("""
            SELECT COUNT(*) as cnt
            FROM clothes_tags
            WHERE c_id=?
        """, (c_id,))[0]["cnt"]
        #
        # print "[TB count]: %d" % (count)

        if count > self.tag_limit:
            return "[]"

        a_tags = tags.strip().split(",")
        a_list = []

        # print a_list

        for a_tag in a_tags:
            a_list.append( (c_id, a_tag, c_id, a_tag) )

        self._db.qry_many("""
            INSERT INTO clothes_tags(c_id, tag)
            SELECT ?,?
            WHERE NOT EXISTS(SELECT tag FROM clothes_tags WHERE c_id=? AND tag=?)
        """, a_list)

        return self._db.qry("SELECT * FROM clothes_tags WHERE c_id=?", (c_id,))


    # Returns video id
    def get_video(self, id):
        self._log.debug("id is: %s", (id))

        path = self._db.qry("SELECT thumbnail FROM clothes WHERE id=?", (id,))[0]['thumbnail']
        path = path.split(".")

        return path[0] + ".mp4"


    def get_smart(self, query, lim, ofs):
        d_codes = ["business-casual", "casual", "formal", "sportswear"]

        # return self._db.qry("SELECT * FROM sqlite_master WHERE type = 'index';")

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

        w_rng = self.weather.w_temp_range()[0]
        w_temp = self._db._temp_group(w_rng)

        self._log.debug("[DEBUG] Current temperatue: %d", (w_rng))
        self._log.debug("[DEBUG] Temperature Range: %d", (w_temp))

        try:
            d_codes.index(query)
            return self._db.qry(base_qry % ("AND dresscode=?"), (w_temp, w_temp, query, lim, ofs*lim))
        except ValueError:
            return self._db.qry(base_qry % ("AND tags LIKE ?"), (w_temp, w_temp, "%"+query+"%", lim, ofs*lim))
        # except:
        #     return {'error': "TOTAL ERROR"}

    # Get all items

    def get_all(self):
        return self._db.qry("""
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

    def get(self, lim, ofs):
        return self._db.qry("""
            SELECT id, thumbnail, dresscode, t_wears,
                (SELECT group_concat(tag, ', ') as tags
                FROM clothes_tags
                WHERE clothes_tags.c_id = clothes.id
                GROUP BY c_id) as tags
            FROM clothes
            WHERE deleted=0
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """,
            (lim, ofs*lim)
        )

    # Get page items
    def page_count(self, pp):
        all_items = self._db.qry("SELECT COUNT(*) as ct FROM clothes")[0]["ct"]

        return all_items/pp

    # Get item by id
    def get_item(self, id):
        return self._db.qry("""
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
    def worn(self, id):
        self._db.qry(
            "UPDATE clothes SET t_wears=t_wears+1 WHERE id=?",
            (id, )
        )
        self._db.qry(
            "INSERT INTO clothes_meta (c_id, temperature, t_time) VALUES (?, ?, date('now'))",
            (id, self.weather.w_current_temp(), )
        )

        return ""
        # return self._db.qry("SELECT * FROM clothes_meta")
        # return self.weather.w_current_temp()

    # Get items meta
    def get_meta(self):
        return self._db.qry("""
            SELECT * FROM clothes_meta
        """)

    def worn_tmp(self, c_id, w, dt):
        self._db.qry(
            "UPDATE clothes SET t_wears=t_wears+1 WHERE id=?",
            (c_id, )
        )

        self._db.qry(
            "INSERT INTO clothes_meta (c_id, temperature, t_time) VALUES (?, ?, ?)",
            (c_id, w, dt,)
        )

    # Like item (ID of element, Like state (0) for no, (1) for yes)
    def set_like(self, id, like):
        self._db.qry(
            "UPDATE clothes SET liked=? WHERE id=?",
            (id, like, )
        )

    def delete(self, id):
        self._db.qry("DELETE FROM clothes WHERE id=?", (id, ))
        self._db.qry("DELETE FROM clothes_meta WHERE id=?", (id, ))
        self._db.qry("DELETE FROM clothes_tags WHERE id=?", (id, ))

    # NOTE: Testing data fill
    def fill_junk(self):
        d_codes = ["business-casual", "casual", "formal", "sportswear"]

        d_tags = ["clubwear", "meetups", "beach", "work", "time", "special", "bugs", "whatistag", "needhelp", "surprise", "nonono", "whatelse"]

        # Clear out clothes table
        self._db.qry("DELETE FROM clothes")
        self._db.qry("VACUUM")
        self._db.qry("DELETE FROM sqlite_sequence WHERE name='clothes'")

        # Clear out clothes meta table
        self._db.qry("DELETE FROM clothes_meta")
        self._db.qry("VACUUM")
        self._db.qry("DELETE FROM sqlite_sequence WHERE name='clothes_meta'")

        # Clear out clothes tags table
        self._db.qry("DELETE FROM clothes_tags")
        self._db.qry("VACUUM")
        self._db.qry("DELETE FROM sqlite_sequence WHERE name='clothes_tags'")

        for i in range(1,100):
            # print random.choice(d_codes)
            self.add(random.choice(d_codes), "thum%s.jpg"%str(random.randint(1,13)))
            i_id = self._db.last_id()

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

    # EDIT dresscode
    def edit_dresscode(self, c_id, dresscode):
        self._db.qry("UPDATE clothes SET dresscode=? WHERE id=?", (dresscode, c_id, ))
        # return "[]"
