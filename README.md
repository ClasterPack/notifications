***
**_Read this in other languages: [English](README.md), [Русский](README.ru.md)_**
***

# API for mailing management service, administration and statistics.

## This is testcase for python junior programmer:

## Main tusk:
Design and develop a service that, according to the given rules, launches a mailing list according to a list of clients.
 **The "distribution" entity has the following attributes:**
 - unique mailing id
 - date and time of the mailing start
 - text of the message to be delivered to the client
 - filter properties of clients to which the mailing should be made (mobile operator code, tag)
 - date and time of the end of the mailing: if for some reason we did not manage to send out all the messages - no messages to the clients after this time should be delivered

**Entity "client" has attributes:**
 - unique client id
 - customer's phone number in the format 7XXXXXXXXXX (X is a number from 0 to 9)
 - mobile operator code
 - tag (arbitrary label)
 - Timezone

**Entity "message" has attributes:**
 - unique message id 
 - date and time when created and sent
 - message status
 - id of the distribution within which the message was sent
 - id of the client to whom it was sent

**Design and develop API for:**
 - CRUD operations for client(create new , read, update , delete client data)
 - creat new distribution witch all it attributes
 - obtaining general statistics on the created mailing lists and the number of sent messages on them, grouped by status
 - obtaining detailed statistics of sent messages for a specific mailing list
 - update distribution attributes
 - delete distribution 
 - processing active mailings and sending messages to customers

**Distribution logic**
 - after creating a new distributio, if the current time is greater than the start time and less than the end time,
all clients that match the filter values specified in this distribution must be selected from the directory 
and sending is started for all these clients.
 -  if distribution is created with a start time in the future,
the sending should start automatically after this time comes without additional actions from the system user.
 - in the course of sending messages, statistics should be collected (see the description of the "message" entity above)
for each message for subsequent reporting.
 - An external service that receives sent messages can process a request for a long time, respond with incorrect data,
or not accept requests at all for some time. It is necessary to implement the correct handling of such errors.
Problems with the external service should not affect the stability of the developed mailing service.

**All tests are in :**
>distribution/tests

**When the API is pushed, there is a link to all methods [docks](http://localhost:8000/docs/)**
 
**[Link for a exercise (in Russian)](https://www.craft.do/s/n6OVYFVUpq0o6L)**

## Working environment

To start development, you need to set up a working environment.

We need the following system dependencies:
- [python](https://www.python.org/downloads/) version 3.10.6 
- Dependency manager [poetry](https://python-poetry.org/docs/#installation) version 1.2.0
- Environment setup:
1. Set up a repository:
    ```shell script
   git clone https://github.com/ClasterPack/notifications.git notifications
   cd notifications
    ```
   
2. Connecting a virtual environment:
   ```shell script
   poetry shell
   ```
   
3. Install dependencies. Dependencies are installed in the virtual environment.
    ```shell script
    poetry install
   ```
   If necessary, install a build with testing environment:
   ```shell script
   poetry install -E devtools
   ```
   
4. Fill in the required data in the .evn file:
```
TOKEN = '<your bearer token>'
   ```

5. Create and apply migrations to the database:
   ```shell script
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start Django server:
   ```shell script
   python manage.py runserver
   ```
7. Start redis-server if needed:
   ```shell script
   redis-server --port 6379
   ```

8. Launch Celery task manager::
   ```shell script
   celery -A notification_service worker -l info -E
   ```
9. Start monitoring Celery using Flower. You can track [here](http://localhost:5566/):
   ```shell script
   celery -A notifications flower --port=5566
   ```
API links:

http://0.0.0.0:8000 - Main Page

http://0.0.0.0:8000/clients - Clients

http://0.0.0.0:8000/distribution - Distributions

http://0.0.0.0:8000/message - Messages

http://0.0.0.0:8000/docs - Swagger docs

http://0.0.0.0:5555 - Flower


### Completed the following additional tasks:
- organize testing of the written code
- make it so that the page with Swagger UI opens at /docs/ and it displays a description of the developed API.
- implement an administrator Web UI to manage mailing lists and get statistics on sent messages
- prepare docker-compose to start all project services with one command
