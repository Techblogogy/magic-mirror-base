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

    @classmethod
    def get_all(self):
        return db.qry("SELECT name, thumbnail, dresscode, tags FROM clothes WHERE deleted=0")

# clothes.setup()
# clothes.add("casual", "1.png", "somthing 1", "cool, winter")
# print clothes.get_all()[0]['dresscode']
