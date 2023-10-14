# Run Project:

$ git clone https://github.com/ukUroojKhan/Project-Django.git

###### Make an Environment
$ pip install virtualenv

$ virtualenv env

###### Activate your Environment
$ .\env\Scripts\activate

###### Use the pip install -r requirements.txt command to install all of the Python modules and packages listed in your requirements.txt file.

note: yor should be on the same dir as requirements.txt file 

$ pip install -r requirements.txt

###### It will save all your python libraries with current version into requirements.txt
$ pip freeze > requirements.txt

###### Run this command if there any changes in DB
$ python manage.py makemigrations
$ python manage.py migrate

###### Run this command to run server
$ python manage.py runserver (copy this link & paste on your browser http://127.0.0.1:8000/)
