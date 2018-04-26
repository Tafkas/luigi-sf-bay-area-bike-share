import os
import time

import luigi
import psycopg2
from luigi.contrib.postgres import PostgresTarget

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


class LoadStationData(luigi.Task):

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

        stations = []
        with open('data/station.csv', 'r') as f:
            next(f)
            for line in f:
                stations.append(tuple([x.strip() for x in line.split(',')]))
        cur.executemany("""INSERT INTO station VALUES (%s,%s,%s,%s,%s,%s,%s)""", stations)

        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='station', update_id='id')


class LoadStatusData(luigi.Task):

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

        statuses = []
        with open('data/status10k.csv', 'r') as f:
            next(f)
            for line in f:
                statuses.append(tuple([x.strip() for x in line.split(',')]))
        cur.executemany("""INSERT INTO status VALUES (%s,%s,%s,%s)""", statuses)

        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='status', update_id='station')


class LoadWeatherData(luigi.Task):

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

        weather = []
        with open('data/weather.csv', 'r') as f:
            next(f)
            for line in f:
                weather.append(tuple([x.strip() for x in line.split(',')]))
        weather = [None if len(x) == 0 else x for x in weather]
        cur.executemany("""INSERT INTO weather VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", weather)


        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='weather', update_id='date')


class LoadTripData(luigi.Task):

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

        trips = []
        with open('data/trip10k.csv', 'r') as f:
            next(f)
            for line in f:
                trips.append(tuple([x.strip() for x in line.split(',')]))
        cur.executemany("""INSERT INTO trip VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", trips)
        conn.commit()
        conn.close()

    def output(self):
        return PostgresTarget(host=HOST, database=DATABASE, user=USER,
                              password=PASSWORD, table='trip', update_id='id')


class FinishPipeline(luigi.Task):
    """Finishes up the pipeline and removes temporary files"""

    def requires(self):
        return [LoadStationData(), LoadWeatherData(), LoadStatusData(), LoadTripData()]

    def run(self):
        tmp_files = ['/tmp/luigi/pipeline', '/tmp/luigi/tables']
        for tmp_file in tmp_files:
            if os.path.isfile(tmp_file):
                os.remove(tmp_file)


if __name__ == '__main__':
    luigi.run(main_task_cls=FinishPipeline)
