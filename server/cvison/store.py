from dbase.dbase import dbase as db
from api_cal.weather import Weather

import random

class clothes:

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
        db.qry(
            "INSERT INTO clothes(name, thumbnail, dresscode) VALUES (?, ?, ?)",
            (name, thumbnail, dresscode, )
        )

    # Add Tags to items
    @classmethod
    def add_tags(self, c_id, tags):
        a_tags = tags.strip().split(",")
        a_list = []

        for a_tag in a_tags:
            a_list.append( (c_id, a_tag) )
        # return a_list

        db.qry_many(
            "INSERT INTO clothes_tags (c_id, tag) VALUES (?, ?)",
            a_list
        )

        return db.qry("SELECT * FROM clothes_tags")

    # TODO: Remove tags from items
    @classmethod
    def rmv_tags(self, id):
        pass

    # TODO: Returns page count
    @classmethod
    def pages(self):
        pass

    @classmethod
    def get_smart(self):
        # db.qry("""
        #     CREATE INDEX t_inx ON clothes_meta (
        #         temp_group(temperature) DESC
        #     )
        # """)

        c_items = db.qry("""
            SELECT
                id, thumbnail, dresscode, t_wears, liked,
                    (SELECT group_concat(tag, ', ') as tags
                    FROM clothes_tags
                    WHERE clothes_tags.c_id = clothes.id
                    GROUP BY c_id) as tags
            FROM clothes
            WHERE deleted=0
            ORDER BY liked DESC, t_wears DESC
        """)

        w_rng = 12 # Weather.w_temp_range()[0]
        w_temp = db._temp_group(w_rng);

        print "[DEBUG] Current temperatue: %d" % (w_rng)
        print "[DEBUG] Temperature Range: %d" % (w_temp)

        # print ((abs(w_rng/5)*10)+1)*db._sign(w_rng)
        # return db.qry("""
        #     SELECT
        #         temp_group(temperature) as tmp, count(*) as tmp_count
        #     FROM clothes_meta
        #     WHERE tmp <= ?
        #     GROUP BY tmp
        #     ORDER BY
        #         CASE tmp
        #             WHEN ? THEN 0
        #             ELSE 1
        #         END, tmp DESC, tmp_count DESC
        # """, (  db._temp_group(w_rng), db._temp_group(w_rng) ) )

        # Get meta tags
        for i in c_items:
            # i['meta'] = db.qry("""
            #     SELECT
            #         t_time, temperature
            #     FROM clothes_meta
            #     WHERE c_id=?
            #     ORDER BY t_time DESC
            # """, (i['id'], ) )

            i['meta'] = db.qry("""
                SELECT
                    temp_group(temperature) as tmp, count(*) as tmp_count
                FROM clothes_meta
                WHERE c_id=? AND tmp <= ?
                GROUP BY tmp
                ORDER BY
                    CASE tmp
                        WHEN ? THEN 0
                        ELSE 1
                    END, tmp DESC, tmp_count DESC
            """, (  i['id'], db._temp_group(w_rng), db._temp_group(w_rng) ) )

        # return db.qry("""
        #     SELECT
        #         *
        #     FROM clothes_meta
        # """)

        return db.qry("""
            SELECT
                CASE
                    WHEN temp_group(temperature) = ? THEN 2
                    WHEN temp_group(temperature) < ? THEN 1
                    ELSE 0 END as temp_rank,
                temp_group(temperature) as temp, temperature
            FROM clothes_meta as cm
            GROUP BY c_id, temp_rank
            ORDER BY temp_rank DESC, temp DESC
        """, (w_temp, w_temp, ))

        return c_items
        # return Weather.w_temp_range()

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

        return db.qry("SELECT * FROM clothes_meta")
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

    # NOTE: Testing data fill
    @classmethod
    def fill_junk(self):
        d_codes = ["business-casual", "casual", "formal", "sportswear"]

        d_tags = ["clubwear", "meetups", "beach", "work", "time", "special ocasion"]

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
