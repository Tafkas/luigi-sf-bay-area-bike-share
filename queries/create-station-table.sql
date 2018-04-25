DROP TABLE IF EXISTS station CASCADE;

CREATE TABLE station (
  id                INTEGER PRIMARY KEY,
  name              TEXT,
  lat               numeric,
  long              numeric,
  dock_count        INTEGER,
  city              TEXT,
  installation_date DATE
);
