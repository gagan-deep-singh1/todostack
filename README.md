#  todostack

Todostack is a simple and user-friendly to-do list app that helps you manage your tasks and stay organized. With Todostack, you can easily create, edit, and mark your to-dos as complete.


# Features
1. Sign up and sign in to your Todostack account
2. Create and manage your to-do list
3. Edit and mark to-dos as complete

# Getting Started
    
1. Clone the repository or download the zip file
2. Download and install docker and docker-compose from https://www.docker.com/
3. Open the project folder in your terminal and run the following command to start the build of the docker images
    `docker-compose up --build` 
4. After the image is built, you can simply run `docker-compose up` to run the container
5. Once the application is up and running, open your browser and go to http://0.0.0.0:8000/
 to access the application
6. Click on the "Sign Up" button to create a new account.
7. Fill out the sign-up form and click "Sign Up" to complete the process
8. Once you are signed in, you can begin creating and managing your to-do list
9. You can also run tests by running the following command in your terminal
    `docker-compose up` then `docker-compose exec web bash` then `python manage.py test --settings=todostack.settings.test_settings`

# Built With 
1. Django
2. Django Rest Framework
3. Javascript
4. HTML


# Contact
If you have any questions or suggestions, please feel free to contact me at gsingh2464@gmail.com
