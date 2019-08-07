# Interview Calendar

[![Coverage Status](https://coveralls.io/repos/github/Telewa/InterviewCalendar/badge.svg?branch=master)](https://coveralls.io/github/Telewa/InterviewCalendar?branch=master)

This is an application which provides an API for an interview calendar.
There are interviewers and candidates. Each interview may consist of exactly one candidate and one or more interviewers.
* If there are more interviewers available than candidates, the spare interviewers are distributed evenly across candidates. (This can be done with the provided api). It's a functional requirement
An interview can only start on the hour.
1. Interviewers can add slots when they have time independently from each other
2. Candidates can add slots when they have time independently from each other
3. Anyone can retrieve a collection of slots when interviews can take place. 

The API
allows the caller to optionally define the candidate and optionally to define one or more interviewer. The API requires either the candidate or the interviewer(s) to be set

### To Run tests
```docker-compose run server python manage.py test```

### Here are postman collections to manual tests
https://www.getpostman.com/collections/9b53e6e699aac4b0f3fd

The test file:
```apps_dir/interview_calendar/tests/test_api.py```
provides a good starting point as far as integration with a front end is concerned.

The following are needed:

In the directory called backend
1. ```docker-compose up``` a super user will be automatically created username = admin/ password = admin. Change this.
2. Sign up some users as demostrated in the test file
3. The postman collection above has some initial payloads which can be used.

Using the API provided a workflow can be created around to actually achieve a fully functional Interview Calendar.
Sample front end work in ongoing in React JS (This was an opportunity to learn react js)
 To view the front end so far, just run: ```yarn start```
 
### Notes
- A lot of cleanup can be done (as shown by the lots of TODO's inline)
- The API provided satisfies all the requirements of the task
- The front end is ages behind in development.
- The database isn't using a volume. Made it easier for development. But in production, a volumne will be absolutely necessary. Configuring this is trivial.
- To handle more traffic realiably:
	- A queueing system, e.g rabbitMQ could be used. This would basically make it all async.
	- have actual separate machiches running the application layer work to increase availability
	- gunicorn could be run using gevent workers (Async). The performance improvement would be immense


### Important goodies
- The application layer is stateless. It can therefore easily scale up and down with traffic/load
- The backend and front end are completely decoupled, to illustrate that there could be myriad of front ends all working with this backend
