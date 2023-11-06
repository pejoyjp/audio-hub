# Before you start

With __macOS__, create a python environment with ```python -m venv <directory/you/want>``` and activate it with ```source <directory/you/want>/bin/activate```. 

With __Windows__, create a python environment with ```python -m venv <directory/you/want>``` and activate it with ```<directory/you/want>\Scripts\activate```. 

Otherwise, search online how to do it. The version used in development is: Python 3.11.6.

----
Run ```pip install -r requirements.txt``` to install all the modules needed to run the project. 

> **Warning:** During your developement, if you need a new module not found in ```requirements.txt``` remember to add it there!


In order to have the proper database configuration, run ```docker-compose up --build -d``` from the ```AudioHub/backend``` folder. To do this you obviously need to have docker installed and running.

> **Warning:** Remember to add to ```.gitignore``` all files that should not be added to the GitHub repository!!

# Structure

The code files can be found in the ```src``` folder. Let's look at a brief description of what should go into each file:

* `__init__.py`
    
    This file is empty. It just tells Python that src with all its modules is a package.

* `database.py`

    It contains the information about the database (where to find it), and creates a session, as well as `sqlalchemy`'s Base class.

* `models.py`

    It defines `sqlalchemy`'s "models" that refer to classes and instances that interact with the database.

    It describes the database's schema: tables, columns and relationships.

* `shcemas.py`

    Defines `pydantic`'s models. They define a data shape

* `crud.py`

    In this file we have reusable functions to interact with the data in the database. That is, Create, Read, Update and Delete operations. 
    
    This is the file where your functions interact with the database. All other files that wish to work with the DB's data, will need to use the functions in this class.

* `main.py`

    This file contains the endpoints that will be accessed by other services.

For more information, visit https://fastapi.tiangolo.com/tutorial/sql-databases/ .
