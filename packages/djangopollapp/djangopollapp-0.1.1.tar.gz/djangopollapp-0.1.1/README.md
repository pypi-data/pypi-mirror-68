# Django Poll App

A simple polls application

## Requirements
- Python >= 3.5.2
- Django 2.2.10
- Django REST framework 3.11.0

## Installation
Install using pip...

```sh
pip install djangopollapp
```
Add the following to your settings.py module:

```sh
INSTALLED_APPS = [
    ...
    'djangopollapp',
]

MIDDLEWARE = [
    ...
    'djangopollapp.middleware.PollMiddleware',
]
```
Include polls api to your urls.py:

```sh
    # Polls API
    url('^api-polls/', include('djangopollapp.api.urls'))
```
and
```sh
./manage.py migrate
```

## Testing the Setup

Example superuser authentication:
```sh
curl -X POST -d "username=<username>&password=<password>" http://127.0.0.1:8000/api-token-auth/

# Response from DRF
{"token":"dfaef188d5f075802cf7b627a41e4dd3632d127b"}%  
```

After that we can create poll without questions:
```sh
curl -X POST -H "Authorization: Token <token>" 
-H "Content-Type: application/json" 
-d '{"poll":
        {
            "title":"Sample",
            "end_date":"2021-05-13T21:25:46Z",
            "description":"sample discript"
        }
    }' http://127.0.0.1:8000/api-polls/v1/polls/
    
# Response axample
{
    "id":1,
    "author":1,
    "title":"Created-poll",
    "start_date":"2020-05-15T06:41:04.837196Z",
    "end_date":"2021-05-13T21:25:46Z",
    "description":"some descript",
    "is_active":true,
    "questions":[]
}
```

## Documentation

### For clients

#### Unique ID

At the first request to the resource, the middleware checks for a unique id in its cookies. 
If the id is not found, the middleware generates a unique id in the format "uu id" and gives the guest user a cookie, 
after which all requests are made with the context of a unique id

#### Polls

***Get all active polls***
```sh
GET http://127.0.0.1:8000/api-polls/v1/polls/

#Response
    {
        "id": 6,
        "author": 1,
        "title": "One more poll",
        "start_date": "2020-05-15T11:36:44.018535Z",
        "end_date": "2021-05-13T21:25:46Z",
        "description": "some description for this poll",
        "is_active": true,
        "questions": null
    },
    {
        "id": 5,
        "author": 1,
        "title": "One more poll",
        "start_date": "2020-05-15T11:36:09.603685Z",
        "end_date": "2021-05-13T21:25:46Z",
        "description": "some description for this poll",
        "is_active": true,
        "questions": null
    },
    ...
]
```

***Get polls by client***, with choice detalization

```sh
GET http://127.0.0.1:8000/api-polls/v1/polls/for-client/

#Response
[
    {
        "id": 7,
        "author": 1,
        "title": "First poll",
        "start_date": "2020-05-15T11:50:09.293380Z",
        "end_date": "2021-05-13T21:25:46Z",
        "description": "some description for this poll",
        "is_active": true,
        "questions": [
            {
                "id": 19,
                "poll": 7,
                "qns": "what?",
                "qns_type": 1,
                "choices": null
            },
            {
                "id": 20,
                "poll": 7,
                "qns": "when?",
                "qns_type": 2,
                "choices": [
                    {
                        "id": 25,
                        "qns": 20,
                        "text": "Today",
                        "vote_counter": 0,
                        "selected": true
                    },
                    {
                        "id": 26,
                        "qns": 20,
                        "text": "Еomorrow",
                        "vote_counter": 0,
                        "selected": false
                    }
                ]
            },
            {
                "id": 21,
                "poll": 7,
                "qns": "where?",
                "qns_type": 3,
                "choices": [
                    {
                        "id": 27,
                        "qns": 21,
                        "text": "here",
                        "vote_counter": 0,
                        "selected": true
                    },
                    {
                        "id": 28,
                        "qns": 21,
                        "text": "there",
                        "vote_counter": 0,
                        "selected": true
                    }
                ]
            }
        ]
    }
]
```
___

***To answer***

We transfer the list of objects.
Attributes of each object: 
***question id, question type and selected options / text***

```sh
POST http://127.0.0.1:8000/api-polls/v1/polls/{id}/to-answer/

#data
[
	{
	    "id": 19,
	    "qns_type": 1,
	    "choices": {"text": "Some text"}
	},
	{
	    "id": 20,
	    "qns_type": 2,
	    "choices": 25
	},
	{
	    "id": 21,
	    "qns_type": 4,
	    "choices": [27, 28]
	}
	...
]

#Response
HTTP Status 201 OK
```

___

### For admins

#### Authorization

Uses standard token authorization from drf
***All requests except get require authorization***

```sh
curl -d '{"username": <username>,"password": <password>}' -H "Content-Type: application/json" -X POST http://127.0.0.1:8000/api-token-auth/

#Response
{"token":"dfaef188d5f075802cf7b627a41e4dd3632d127b"}
```
---

#### Polls
    
***Create***

A poll is created in two parts:
- Poll data
- Question data

Each question has its own type.
- 1 - Text answer
- 2 - Single Choice
- 3 - Multi Choice

If question type is 1(Text answer), choices field must be empty.
If question type is 2(Single Choice) or 3(Multi Choice), choices field will be a include choice objects

In the data of each question, we also put choices depending on its type
```sh
curl http://127.0.0.1:8000/api-polls/v1/polls/ \
-X POST \
-H "Authorization: Token dfaef188d5f075802cf7b627a41e4dd3632d127b" \
-d '{
  "poll": {
    "title": "One more poll",
    "end_date": "2021-05-13T21:25:46Z",
    "description": "some description for this poll",
  },
  "questions": [
    ...
    {
      "qns": "what the fuck?",
      "qns_type": 1,
      "choices": [
        ...
        {
          "text": "some choice",
        }
      ]
    },
    ...
  ]
}'
```

___

***Update***

You can change one or more fields

Poll

| Editable fields | type | mean |
| ------ | ------ | ------ |
| title | string | Poll title |
| end_date | datetime | Date of end poll |
| description | string | Description |

```sh
PATCH http://127.0.0.1:8000/api-polls/v1/polls/{id}/

#Response
{
    "id": 7,
    "author": 1,
    "title": "First poll",
    "start_date": "2020-05-15T11:50:09.293380Z",
    "end_date": "2021-05-13T21:25:46Z",
    "description": "some description for this poll!!!",
    "is_active": true,
    "questions": [
        {
            "id": 19,
            "poll": 7,
            "qns": "what?what?",
            "qns_type": 1,
            "choices": null
        },
        ...
    ]
}
```

Question

| Editable fields | type | mean |
| ------ | ------ | ------ |
| poll | int | related poll |
| qns | string | question |
| qns_type | int | 1 - text, 2 - single choice,
| | | 3 - multi choice |


```sh
PATCH http://127.0.0.1:8000/api-polls/v1/question/{id}/

#Response
{
    "id": 19,
    "poll": 7,
    "qns": "what?",
    "qns_type": 1,
    "choices": null
}
```

***Delete***

Poll
```sh
DELETE http://127.0.0.1:8000/api-polls/v1/polls/{id}/

#Response
HTTP Status 204 No Content
```

Question
```sh
DELETE http://127.0.0.1:8000/api-polls/v1/questions/{id}/

#Response
HTTP Status 204 No Content
```