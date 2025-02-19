-- Ensure ride_demo schema exists
CREATE SCHEMA IF NOT EXISTS ride_demo;

-- Enable PostGIS in public (default location)
CREATE EXTENSION IF NOT EXISTS postgis SCHEMA public;
CREATE EXTENSION IF NOT EXISTS postgis_topology SCHEMA public;

-- Grant permissions so ride_demo can use public.geography
GRANT USAGE ON SCHEMA public TO PUBLIC;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO PUBLIC;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";

-- Set default search path so ride_demo queries can find public.geography
ALTER DATABASE mydb SET search_path TO ride_demo, public;
