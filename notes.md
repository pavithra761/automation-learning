#Day 1:
- Trigger: the event that starts the automation.
- Action: a step it performs after starting.
- Filter: a rule that stops the run if a condition isn't met.
- Data mapping: choosing which data goes into which field of the next step.
- Run history: the log of past runs and what happened in each step.

used zapier for automated email responses from google forms that are submitted.
trigger was the google form submition
action taken wen the sheets were filled with data and mail sent to host
data mapping: sending the info mapping it with requiremennts





Day 2: Api(application programming interface) and JSON(javascript objectnotion)

- API:
applicatin proramming interface.
It is a way for two applications to share data.
Mediator for two applications.

- Request: 
asking for what data you require.

- Response: 
What you get back after the request

- Status code: 
The request comes with a code like 2xx(success), 4x(error)x, 5xx(too many requests)

- JSON:
The format of the data

- API key:
a secret key of autentication.

- Rate limit: 
ho many requests you can send in a time period.

POSTMAN APP
This is used to test the api working.
it shows all the behind work how the data is sent and recieved.

created a postaman account and send a git hub url for login details
steps for it?
Go to collections
make a new requst
give the method to PUSH
give the url and send it.

You get back stataus code like 200.
with data in JSON format.(u can also get data in xml,yaml,html formats too)


1.gave a request for get method of weatherforcast.
https://api.open-meteo.com/v1/forecast?latitude=40.7&longitude=-74.0&current_weather=true
the above url:
https a secure protocol with meteo applicatio url.
? this is used for what parameteres your looking for.
path=key (lat and long = values)
You can add more parameteres with & 

2. giving wrong url for error code
404 error
4 stands for error in th url

5xx
server problem

429 too many requests wait for a while

Debugging habit

When a call fails, check in this order:

Did I get a status code at all? If not, check the domain, the internet connection and http versus https.
If I did, which code is it? 4xx means check my request. 5xx means the server has a problem.

3.POST request
This is to send a data
Select post method give the respected url that your sending data.
Then select the body tab below with json format give the data and send

4.GET api with headears
If u need to get a data from a private applications u need to use a key.
send the get with the url and under the headers u specify ur key id and send the get for the data.



CURL
to use to get data from terminal directly

its a command line for postman.
curl is a program line
curl "url"
curl -i url (gives the response header that statsu code)
curl -x
curl -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{"name": "test", "value": 1}'
-x sets the methid to post
-h adds a header like json type aldo the key api.
-d is the body.

- curl URL: GET request
- -i: show headers
- -X POST: set the method
- -H "Key: value": add a header
- -d '...': send a body