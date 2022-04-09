# WTF

Simple device manager to check how's is point on which device in You small company.

Use Django 4 for backend and Bootstrap 5 as fronend.

**ACHTUNG!:** Password for switch to edit mode is hardcoded in simple_auth application, change it if need.

# Depends

| Package           | Version |
|-------------------|:-------:|
|python             | 3.8.10  |
|asgiref            | 3.5.0  |
|backports.zoneinfo | 0.2.1  |
|Django             | 4.0.3  |
|pip                | 20.0.2 |
|pkg-resources      | 0.0.0  |
|PyMySQL            | 1.0.2  |
|setuptools         | 44.0.0 |
|sqlparse           | 0.4.2  |

For install under Linux:
```console
python3 -m venv ./
source ./venv/bin/activate
pip install -r requirements.txt
```

# Installation

**ACHTING!** Change password for access databases from default, if Your network have access to global-net! (in manual of Docker installation and settings.py file)

1. Create volume for MySQL databases `sudo docker volume cretae inv-base-mysql-data`
2. Create container `sudo docker run --name inv-base_database -v inv-base-mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=g0d0fsyst3m -e MYSQL_USER=inv-base -e MYSQL_PASSWORD=usrinv-base -e MYSQL_DATABASE=inv-base-db -p 3306:3306 -d mariadb:10.5`
3. <next steps is under constructions, be patient>
