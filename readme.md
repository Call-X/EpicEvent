
# OpenclassroomProjets - "SoftDesk API"


## Custommer asking:

Epic Events, a company specialising in events.
that caters for the needs of start-ups wanting to organise 'epic' parties.
parties
In this this situation as Software developer backend, my goal were:
- Django application on a PostgreSQL database
- creating login page for users to access
- Non-administrator users can be associated with one of the two groups determining authorisations for the API
- Creating API supporting CRUD operations based on database models
- Creating API endpoints must enable users to search for and filter information

The application shall use the termination points of the API to request and write data.

The documentation of the API is available at the following location: Insomnia-documentater

The API is developped in python using Django Rest Framework.


## Installation guide :
1. Clone the repository 
```
$ git clone https://github.com/Call-X/EpicEvent.git
```
2. Navigate to the root folder of the repository

3. Create a virtual environnement with :
``` 
python -m venv projectenv
```
3. Activate the virtual environment with
``` 
projectenv/Srcipts/activate
``` 
4. install the project with its dependencies with :
``` 
pip install -r requirements.txt
``` 
5. Finally, run the server with :
``` 
python manage.py runserver
``` 

## How to use ?

1. Install Node.js which automaticaly will install the package manager JavaScript NPM

2. Install all dependencies to your project :
```
nmp install
```

4. Get your Insomnia Documentation file in your browser:
```
npx insomnia-documenter --config <Name_of_your_file>.json --output insomnia-final
```
 * * * Done! * * *
Your documentation has been created and it's ready to be deployed!

5. Go to your project.file with the command :
```
cd insomnia-final
```

6. launch with command : 
```
npx serve
``` 

7. Open the following adress on your web browser
```
http://localhost:3000
```
8. Follow the instruction on the Insomnia-Documenter


## Contributeur :

-Emile MIATH -

# Licence & Copyright :

Aucun copyrights



