DROP TABLE IF EXISTS weather;

CREATE TABLE weather (
  date                           DATE,
  max_temperature_f              TEXT,
  mean_temperature_f             TEXT,
  min_temperature_f              TEXT,
  max_dew_point_f                TEXT,
  mean_dew_point_f               TEXT,
  min_dew_point_f                TEXT,
  max_humidity                   TEXT,
  mean_humidity                  TEXT,
  min_humidity                   TEXT,
  max_sea_level_pressure_inches  TEXT,
  mean_sea_level_pressure_inches TEXT,
  min_sea_level_pressure_inches  TEXT,
  max_visibility_miles           TEXT,
  mean_visibility_miles          TEXT,
  min_visibility_miles           TEXT,
  max_wind_Speed_mph             TEXT,
  mean_wind_speed_mph            TEXT,
  max_gust_speed_mph             TEXT,
  precipitation_inches           TEXT,
  cloud_cover                    TEXT,
  events                         TEXT,
  wind_dir_degrees               TEXT,
  zip_code                       TEXT
);
