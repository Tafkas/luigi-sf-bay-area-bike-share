import os
import time

import luigi
from luigi.contrib.postgres import PostgresTarget
import psycopg2

HOST = 'localhost'
DATABASE = 'sfbike'
USER = 'stade'
PASSWORD = ''


class InitialTask(luigi.Task):
    """An initital task to start the pipeline. To enforce ingesting the data remove the tmp file"""

    def requires(self):
        return []

    def run(self):
        time.sleep(10)
        conn = psycopg2.connect(dbname=DATABASE,
                                user=USER,
                                host=HOST,
                                password=PASSWORD)
        cur = conn.cursor()

        sql = "DROP DATABASE sfbike; CREATE DATABASE sfbike;"
        cur.execute(sql)
        conn.commit()
        conn.close()

    def output(self):
        return luigi.LocalTarget('queries/create-tables.sql')

    def exists(self):
        return False


class CreateDatabaseTables(luigi.Task):
    """Creates the database structure"""

    def requires(self):
        return InitialTask()

    def query(self):
        with open('queries/create-station-table.sql', 'r') as f:
            return f.read()

    def run(self):
        conn = psycopg2.connect(dbname=DATABASE,
                                user=USER,
                                host=HOST,
                                password=PASSWORD)
        cur = conn.cursor()

        sql = self.query()
        cur.execute(sql)
        conn.commit()
        conn.close()


class CreateStationTable(luigi.Task):

    def requires(self):
        return InitialTask()

    def query(self):
        with open('queries/create-station-table.sql', 'r') as f:
            return f.read()

    def run(self):
        conn = psycopg2.connect(dbname=DATABASE,
                                user=USER,
                                host=HOST,
                                password=PASSWORD)
        cur = conn.cursor()

        sql = self.query()
        cur.execute(sql)
        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='station', update_id='id')


class CreateStatusTable(luigi.Task):

    def requires(self):
        return InitialTask()

    def query(self):
        with open('queries/create-status-table.sql', 'r') as f:
            return f.read()

    def run(self):
        conn = psycopg2.connect(dbname=DATABASE,
                                user=USER,
                                host=HOST,
                                password=PASSWORD)
        cur = conn.cursor()

        sql = self.query()
        cur.execute(sql)
        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='status', update_id='id')


class CreateWeatherTable(luigi.Task):

    def requires(self):
        return InitialTask()

    def query(self):
        with open('queries/create-weather-table.sql', 'r') as f:
            return f.read()

    def run(self):
        conn = psycopg2.connect(dbname=DATABASE,
                                user=USER,
                                host=HOST,
                                password=PASSWORD)
        cur = conn.cursor()

        sql = self.query()
        cur.execute(sql)
        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='weather', update_id='id')


class CreateTripTable(luigi.Task):

    def requires(self):
        return InitialTask()

    def query(self):
        with open('queries/create-trip-table.sql', 'r') as f:
            return f.read()

    def run(self):
        conn = psycopg2.connect(dbname=DATABASE,
                                user=USER,
                                host=HOST,
                                password=PASSWORD)
        cur = conn.cursor()

        sql = self.query()
        cur.execute(sql)
        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='trip', update_id='id')


class ExtractStations(luigi.Task):
    """Extracts the bike station data and stores it in the database"""
    host = 'localhost'
    database = 'sfbike'
    user = 'stade'
    password = ''
    table = ''

    def requires(self):
        return [CreateStationTable()]

    def run(self):
        stations = []
        with open('data/station.csv', 'r') as f:
            next(f)
            for line in f:
                stations.append(tuple([x.strip() for x in line.split(',')]))

        conn = psycopg2.connect(dbname=self.database,
                                user=self.user,
                                host=self.host,
                                password=self.password)
        cur = conn.cursor()
        cur.executemany("""INSERT INTO station VALUES (%s,%s,%s,%s,%s,%s,%s)""", stations)
        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='stations', update_id='id')


class FinishPipeline(luigi.Task):
    """Finishes up the pipeline and removes temporary files"""

    def requires(self):
        return [ExtractStations(), CreateWeatherTable(), CreateStatusTable(), CreateTripTable()]

    def run(self):
        tmp_files = ['/tmp/luigi/pipeline', '/tmp/luigi/tables']
        for tmp_file in tmp_files:
            if os.path.isfile(tmp_file):
                os.remove(tmp_file)


if __name__ == '__main__':
    luigi.run(main_task_cls=FinishPipeline)
