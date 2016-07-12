from dbase.dbase import dbase as db

class clothes:

    @classmethod
    def setup(self):
        db.qry("""
            CREATE TABLE IF NOT EXISTS clothes (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                thumbnail TEXT NOT NULL,
                dresscode TEXT NOT NULL,
                temperature TEXT NOT NULL,
                tags TEXT,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        """)

    # Add clothing item
    @classmethod
    def add(self, dresscode, thumbnail, name="", tags=""):
        db.qry(
            "INSERT INTO clothes(name, thumbnail, dresscode, tags) VALUES (?,?,?,?)",
            (name, thumbnail, dresscode, tags, )
        )

    # Get all items
    @classmethod
    def get_all(self):
        return db.qry("SELECT name, thumbnail, dresscode, tags FROM clothes WHERE deleted=0")

    # Get letters in range
    @classmethod
    def get(self, lim, ofs):
        return db.qry(
            "SELECT id, name, thumbnail, dresscode, tags FROM clothes WHERE deleted=0 LIMIT ? OFFSET ?",
            (lim, ofs)
        )

# clothes.setup()
# clothes.add("casual", "1.png", "somthing 1", "cool, winter")
# print clothes.get(3,3)
