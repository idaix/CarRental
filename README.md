# AUTORENT
Autorent is an Algerian car rental platform.

This platform is the link between Agencies and the client. 
It helps Agencies to manage the car business and the clients to book vehicles according to their requirements and needs and inquiry about new cars. Both the client and the Agency administrator(s) have different rights from their perspectives as well as different credentials.

Autorent was made by 3 students from Mohamed El Bachir El Ibrahimi University of Bordj Bou Arréridj El-Anasser as a final undergraduate project.

### Overview

![home](./screenshots/finalresult.png)

- Setup
    - Wilaya & Commune
    - Vehicle Make & Model & Type
- Vehicle
    - Vehicle Details
- Agency
    - Register
    - Agency Profile
    - Update profile
    - Delete profile
    - Dashboard *See & manage vehicles*
    - Add vehicle
    - Update vehicle
    - Delete Vehicle


### Run `AUTORENT`  in your local machine
 Setup envirnement
 
	py venv -envname-
Install django

	pip install django
Install dependencies

	pip install Pillow
	pip install django-crispy-forms
Clone repository

    git clone git@github.com:daishek/CarRental.git
    cd CarRental
Migrate

    py .\manage.py migrate
    py .\manage.py loaddata wilaya.json
    py .\manage.py loaddata commune.json
    py .\manage.py loaddata makes.json
    py .\manage.py loaddata models.json
    py .\manage.py loaddata energy.json
    py .\manage.py loaddata transmission.json
    py .\manage.py loaddata type.json
    py .\manage.py loaddata type.json
    py .\manage.py loaddata options.json
