import psycopg2
from db.configdatabase import config


class Database:
    def __init__(self):
        self.params = None
        self.conn = None
        self.cursor = None

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            self.params = config()
            print('Connecting to the database...')
            self.conn = psycopg2.connect(**self.params)
            self.cursor = self.conn.cursor()
            print('Connected')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')

    def save(self, serverstatus: dict):
        for k, v in serverstatus.items():
            self.cursor.execute(f"insert into servers (site, status) values ('{k}', '{v}')")
            self.conn.commit()
            print(f"'{k}': '{v}' has been added to db")

    def save_many(self, serverstatuslist: list):
        for server in serverstatuslist:
            self.save(server)

    def close(self):
        self.cursor.close()
        self.conn.close()
