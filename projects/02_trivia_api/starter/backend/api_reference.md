# Trivia API Reference

## Introduction
The Trivia API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.
## Getting started
### Base URL
At present the Trivia  api can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`
### Authentication: 
This version of the application does not require authentication or API keys. 

## Error Handling
Errors are returned as JSON objects in the following format:
Example for '`404: resource not found`' error:

```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return two error types when requests fail:

- 404: resource not found
- 422: Unrocessable 
- 400: Bad request

## Endpoints :

### GET '/categories'
- General : return a list of categories objects, and success value. each category object contains a category type and its corresponding id.
- Sample : 
```bash
 curl http://127.0.0.1:5000/categories
 ```
 Output:
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET '/questions'
- General: returns a list of questions object, success value, number of total questions, and categories object
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample :
```bash 
curl http://127.0.0.1:5000/questions
```
Output
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendag
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
- Sample 2 : page 2
```bash
curl http://127.0.0.1:5000/questions?page=2
```
Output
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Algeria",
      "category": 3,
      "difficulty": 1,
      "id": 24,
      "question": "What is the biggest country in Africa?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
### GET '/categories/{category_id}/questions'
- General : returns a list of success value, number of questions for the specefic category, number of total questions, and an object of the category's questions.
- Sample:
```bash
curl http://127.0.0.1:5000/categories/1/questions
```
Output
```
{
  "category_questions": 3,
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 26
}
```
### POST '/questions/search'
- General : search for question(s) using a search term. Returns a list of success value, the search term, matching results questions object, and number of total questions.
- Sample :
```bash
curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm":"egypt"}'
```
On windows ```CMD``` make sure to send the correct json format, follow this Sample :
```bash
curl -X POST http://127.0.0.1:5000/questions/search -H "Content-Type: application/json" -d "{\"searchTerm\":\"egypt\"}"
```
Output
```
{
  "questions": [
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "searched": "egypt",
  "success": true,
  "total_questions": 26
}
```
### POST '/questions'
- General: Creates a new question by submitting the question, answer, difficulty level, and the corresponding category.
it returns a list of success value, the id of the created question, and number of total questions.
- Re-Creating an existing question is not allowed.
- Sample:
```bash
curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"UEFA Champions League top goalscorer?","answer":"Cristiano Ronaldo","difficulty":"3","category":"6"}"
```
If you are using windows ```CMD``` use this format :
```bash
curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"question\":\"UEFA Champions League top goalscorer?\",\"answer\":\"Cristiano Ronaldo\",\"difficulty\":\"3\",\"category\":\"6\"}"
```
Output:
```bash
{
  "created": 34,
  "success": true,
  "total_questions": 28
}
```

### DELETE '/questions/{question_id}'
- General: Deletes the question of the given ID if it exists.
It returns the success value, the ID of the deleted question and the number of the total questions.
- Sample:
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
Output:
```
{
  "deleted": "10",
  "success": true,
  "total_questions": 27
}
```





