# Bibliophile
Web application for searching for libraries and book shops in Washington, DC. App supports crowdsourcing of community edits and additions to the list. 

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app1.png)


SQLite Database is populated with results from an Open Street Map (OSM) query for bookshops and libraries. So that others could repurpose this application for other cities or points of interest, I created  separate Python class for running OSM queries based on different locations and key:value pairs. 

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app2.png)


After registering or logging in, an edit icon appears next to each item in the list.

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app3.png)

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app4.png)


Users can also create new entries in the database. 

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app5.png)


The database just includes two tables, one for the book locations and one for users. User passwords are hashed and salted multiple times. 

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app6.png)


Here is a screenshot of the OSM query class, which relies on the Overpass Turbo query engine (https://overpass-turbo.eu/).

![app_screenshot](https://github.com/Holly-Transport/Bibliophile/blob/master/screenshots/app7.png)
