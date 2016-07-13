from dbase.dbase import dbase as db

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
                tags TEXT,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        """)

        # Clothes Metadata Table (add value when item is worn)
        db.qry("""
            CREATE TABLE IF NOT EXISTS clothes_meta (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                c_id INTEGER NOT NULL,

                temperature INT NOT NULL,
                t_time TEXT DEFAULT date('now')
            )
        """)

    # Add clothing item
    @classmethod
    def add(self, dresscode, thumbnail, name="", tags=""):
        db.qry(
            "INSERT INTO clothes(name, thumbnail, dresscode, tags) VALUES (?, ?, ?, ?)",
            (name, thumbnail, temperature, dresscode, )
        )

    # Get all items
    @classmethod
    def get_all(self):
        return db.qry("SELECT name, thumbnail, dresscode, temperature, t_wears, tags FROM clothes WHERE deleted=0")

    # Get items in range
    @classmethod
    def get(self, lim, ofs):
        return db.qry(
            "SELECT id, name, thumbnail, dresscode, t_wears, tags FROM clothes WHERE deleted=0 LIMIT ? OFFSET ?",
            (lim, ofs)
        )

    # Mark item as worn
    @classmethod
    def worn(self, id):
        db.qry(
            "UPDATE clothes SET t_wears=t_wears+1 WHERE id=?",
            (id, )
        )

clothes.setup()
clothes.add("casual", "1.png", 20, "somthing 1", "cool, winter")
clothes.worn(1)
print clothes.get_all()
