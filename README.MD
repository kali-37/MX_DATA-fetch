# Below settings are linux friendly as made for hosting , but windows normal can also do setup surfing internet . 


* Install <b>mysql</b>, <b>mysql-server</b> and <b><i>(rabit mq)</i> used to automate task in background </b> in linux , if windows search online and install this two mysql and rabit mq 
- for linux user you can go as follows also install dependencies

        sudo apt update
        sudo apt upgrade
        sudo apt install mysql
        sudo apt install rabbitmq-server
        sudo service rabbitmq-server start
        sudo service mysql start

* Enable both to auto start during startup in linux , in windows you can use task manager  

        sudo systemctl enable mysql 
        sudo rabbitmq-plugins enable rabbitmq_management
        sudo systemctl enable rabbitmq-server





To set up a user in the database, follow these steps:

Create a user named <b>'SQL_MX'</b> with the password 'root'. If you have changed the password, make sure to update it in the 'Setting.py' section.

Create a database named <b>"MX_DATABASE1".</b>

Grant all privileges to the user 'SQL_MX' for the database "MX_DATABASE1".

That's it! You have now created the user 'SQL_MX' in the database with the appropriate privileges for the "MX_DATABASE1" database.

* Settings.py in our /tempcsv/MX_RECORD/MX_RECORD

             DATABASES = {
                 'default': {
                     'ENGINE': 'django.db.backends.mysql',
                     'NAME': 'MX_DATABASE1',
                     'USER': 'SQL_MX',
                     'PASSWORD': 'root',  # change password here , if you don't put it 'root' 
                     'HOST': 'localhost',
                     'PORT': '3306',
                  },   
             }










## Unzipping the folder 
Unzipping in Windows:

* Using File Explorer:

    Locate the zip file in File Explorer.
    Right-click on the zip file and select "Extract All" from the context menu.
    Choose the destination folder where you want to extract the files and click "Extract".

* using linux or hosting

        unzip PROJECT.zip


* Now use linux terminal or windows powershell , recommend linux 
  command may vary so you can  serarch in google , AI source etc.

        cd tempcsv

* Activate the serve enviroment , make sure bin folder is there in current dir 

        source bin/activate      

* Install requirments 

        pip install -r requirments.txt 



* After the mysql is setup and rabit mq, go to directory 
** To create migrations of database , do write below commands in directory : <b> /tempcsv/MX_RECORD
</b>
 
        python manage.py makemigrations 
        python manage.py migrate





Now create celery worker background process in linux as per your configuration of system,Else you start it manually using terminal below command.

* For log we can use flag --loglevel=info else not .

            celery -A MX_RECORD  worker --loglevel=info



Now also start celery beat as 

            celery -A MX_RECORD  beat --loglevel=info

Also start python manage.py runserver as below at path /tempcsv/MX_RECORD

            python manage.py runserver 


Configure nginx as per enviroment setup  you can search this stuffs online how to do or handel by the hoster developers themself.


# Admin and other user importance 



In the system, the admin section is accessible only to the **super user**, who has full control and can perform various tasks. The super user is essentially the root or administrator of the system. Additionally, there are two other users: **operator 1** and **operator 2**.

- **Operator 1**: This user has limited access and can only handle the import section job. They do not have staff access and cannot perform other tasks or access the admin section.

- **Operator 2**: This user has access to both the import section and other functionalities, but they are restricted from deleting data.

The super user, being the admin, has the ability to change passwords for any user, including themselves.

Please note that it's important for the super user to be familiar with the system and understand how to operate and manage different functionalities within the admin panel.


# Important Considerations

- When working with API calls, it's essential to handle the import section with care. Here are a few important points to remember:

- Data Import Limit: If your API has a monthly limit of 20,000 calls, it's advisable to import only a subset of data, such as 2,000 records, before starting the process. By doing this, you can ensure that you stay within your allotted quota.

- Celery Beats and Celery Worker: To manage the import process efficiently, it's recommended to utilize Celery Beats and Celery Worker. These tools allow you to schedule and execute tasks asynchronously, ensuring that only the specified amount of data is considered and stored in the API.

- Continuous Execution: While running Celery Worker and Celery Beats continuously may not be a concern, it's important to keep track of your credits or resources. If your credits are depleted or you encounter any issues, data may be imported without finding any corresponding MX records. Hence, it's crucial to monitor and manage resources effectively.

        By taking these factors into consideration and handling the import section carefully, you can ensure the smooth operation of your API while optimizing resource usage and avoiding any potential issues.

