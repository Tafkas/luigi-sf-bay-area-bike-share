DROP TABLE IF EXISTS trip CASCADE;

CREATE TABLE trip (
  id                 INTEGER PRIMARY KEY,
  duration           INTEGER,
  start_date         TIMESTAMP WITH TIME ZONE,
  start_station_name TEXT,
  start_station_id   INTEGER,
  end_date           TIMESTAMP WITH TIME ZONE,
  end_station_name   TEXT,
  end_station_id     INTEGER,
  bike_id            INTEGER,
  subscription_type  TEXT,
  zip_code           TEXT
);
