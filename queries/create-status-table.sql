DROP TABLE IF EXISTS status CASCADE;

CREATE TABLE status (
  station_id      INTEGER,
  bikes_available INTEGER,
  docks_available INTEGER,
  time            TIMESTAMP WITH TIME ZONE
);
