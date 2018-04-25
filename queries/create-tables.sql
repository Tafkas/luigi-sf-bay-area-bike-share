DROP TABLE IF EXISTS station CASCADE;
DROP TABLE IF EXISTS status CASCADE;
DROP TABLE IF EXISTS trip CASCADE;
DROP TABLE IF EXISTS weather CASCADE;

CREATE TABLE station (
  id                INTEGER PRIMARY KEY,
  name              TEXT,
  lat               numeric,
  long              numeric,
  dock_count        INTEGER,
  city              TEXT,
  installation_date DATE
);

CREATE TABLE status (
  station_id      INTEGER,
  bikes_available INTEGER,
  docks_available INTEGER,
  time            TIMESTAMP WITH TIME ZONE
);

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

CREATE TABLE weather (
  date                           TIMESTAMP WITH TIME ZONE,
  max_temperature_f              INTEGER,
  mean_temperature_f             INTEGER,
  min_temperature_f              INTEGER,
  max_dew_point_f                INTEGER,
  mean_dew_point_f               INTEGER,
  min_dew_point_f                INTEGER,
  max_humidity                   INTEGER,
  mean_humidity                  INTEGER,
  min_humidity                   INTEGER,
  max_sea_level_pressure_inches  numeric,
  mean_sea_level_pressure_inches numeric,
  min_sea_level_pressure_inches  numeric,
  max_visibility_miles           INTEGER,
  mean_visibility_miles          INTEGER,
  min_visibility_miles           INTEGER,
  max_wind_Speed_mph             INTEGER,
  mean_wind_speed_mph            INTEGER,
  max_gust_speed_mph             INTEGER,
  precipitation_inches           INTEGER,
  cloud_cover                    INTEGER,
  events                         TEXT,
  wind_dir_degrees               INTEGER,
  zip_code                       INTEGER
);
