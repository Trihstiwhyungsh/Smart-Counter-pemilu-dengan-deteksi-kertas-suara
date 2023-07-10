# **The Callisto Protocol**

### Callisto is an webservice for capstone project. This app build on Flask-Restx and Python.

## **Installation**

- ### Clone this project using **Git** or download **zip file**.
- ### Install all required dependencies with **pip** or **pipenv**.
    ```
    pip install -r requirements.txt
    ```
    ### or
    ```
    pipenv install -r requirements.txt
    ```
- ### Migrate database with these command in your terminal.
    ```
    pipenv run python
    >>> from app import db
    >>> db.create_all()
    ```
- ### Run project with natively python or with virtual env like **pipenv**.
    ```
    pipenv run python main.py
    ```
    ### or
    ```
    python main.py
    ```
## **Folder structure**
- ### app -> Core apps
- ### controllers -> Focus to parsing from request and return response
- ### services -> There are business logic
- ### models -> The object model for mapping into database (table and column)
- ### helpers -> There are reusabel function