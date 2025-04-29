# RepairManagements
docker compose up -d --build

docker-compose exec db psql -U postgres
CREATE DATABASE fixenix_edutech;
CREATE USER codefyn WITH PASSWORD 'Illuminati@007;
GRANT ALL PRIVILEGES ON DATABASE fixenix TO codefyn;


CREATE ROLE codefyn WITH LOGIN PASSWORD 'Illuminati@007';
ALTER ROLE codefyn CREATEDB;
ALTER ROLE codefyn WITH SUPERUSER;
docker compse eexec web pyatrhon manage.py migrate
docker compse eexec web pyatrhon manage.py createsuperuser
docker compse eexec web pyatrhon manage.py   add_devices
docker compse eexec web pyatrhon manage.py   add_device_brands
docker compse eexec web pyatrhon manage.py   add_device_mobile_models
docker compse eexec web pyatrhon manage.py   add_device_laptop_models
docker compse eexec web pyatrhon manage.py   add_device_tab_models
docker compse eexec web pyatrhon manage.py   add_device_desktop_models
docker compse eexec web pyatrhon manage.py   add_device_desktop_problems
docker compse eexec web pyatrhon manage.py   add_device_laptop_problems
docker compse eexec web pyatrhon manage.py   add_device_mobile_problems
docker compse eexec web pyatrhon manage.py   add_device_tab_problems
docker compse eexec web pyatrhon manage.py   loaddata services.json# Fixenix_v5
