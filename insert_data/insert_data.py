
import psycopg2
from decouple import config

class InsertData():
    conn = None

    def __init__(self):
        self.init_db_config(config)

    def init_db_config(self, config):
        try:
            self.conn = psycopg2.connect(
                "dbname='backup_genomika'"
                " user='postgres' host='localhost' password='g3n0m1k@'"
            )
            print ("Conectado no Banco com sucesso!")
        except:
            print ("Erro ao conectar a base de dados")

    def insert(self, db_name, column_value):
        cur = self.conn.cursor()
        if db_name == 'core_backup':
            cur.execute(
                u"INSERT INTO"" core_backup "
                "(name, percents_completed, status, start_backup_datetime, "
                "finish_backup_datetime) VALUES "
                "('{0}', {1}, {2}, {3},{4}) RETURNING id".format(
                    column_value['name'],
                    column_value['percents_completed'],
                    column_value['status'],
                    column_value['start_backup_datetime'],
                    column_value['finish_backup_datetime']
                )
            )

        elif db_name == 'core_backuplog':
            cur.execute(
                u"INSERT INTO"" core_backuplog "
                "(backup_id, log, success, log_datetime) VALUES "
                "({0}, '{1}', {2}, {3}) RETURNING id".format(
                    column_value['backup_id'],
                    column_value['log'],
                    column_value['success'],
                    column_value['log_datetime']
                )
            )
        pk = cur.fetchone()[0]
        self.conn.commit()

        return pk
    def close_conn(self):
        self.conn.close()


a = InsertData()
col_vl = {
    'backup_id': 1,
    'success': False,
    'log': "Teste",
    'log_datetime': 'now()'

}
a.insert('core_backuplog', col_vl)
a.close_conn()
