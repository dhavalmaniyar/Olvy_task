# Olvy_task

# How to run?

1. Create virtual environment for the project.
  
  Run command:
  ```
   Olvy_task$ c:\>python -m venv c:\path\to\myenv
  ```
  
  Now, enter in myenv:
  For Linux/ Mac OS:
  ```
  Olvy_task$ Source myenv/bin/activate
  ```
  
  For Windows:
  ```
  Olvy_task$ myenv\Scripts\activate
  ```
  
2. Now, install requirements.txt file using:

   ```
   (myenv)Olvy_task$ pip install requirements.txt
   ```
 
   This will install all the dependencies.
    
3. Next is to locate manage.py file and run command to start the django server.
  ```
  Olvy_task$ python manage.py runserver
  ```
  This will available on port no. 8000.
  
4. Now, get inside the ```vueapp/vuedjango``` and run command to start the vue.js server.

  ```
Olvy_task/vueapp/vuedjango$ yarn serve
  ```
This will available on port no. 8080.

5. Now enter the Url to the browser ```http://localhost:8080/``` and get the output.

![](https://github.com/dhavalmaniyar/Olvy_task/blob/main/Screenshot_2022-02-09%20vuedjango.png)
