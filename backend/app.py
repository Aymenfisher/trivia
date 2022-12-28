import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category
from random import choice

QUESTIONS_PER_PAGE = 10
def paginations(request,data):
  page=request.args.get('page',1,type=int)

  start=(page-1)*QUESTIONS_PER_PAGE
  end=start+QUESTIONS_PER_PAGE
  data_list=[i.format() for i in data]
  page_data=data_list[start:end]
  if len(page_data)==0:
    abort(404)

  return page_data

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  cors=CORS(app,resources={r'/*':{'origins':'*'}})


  #@TODO: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():
    try:
      categories=Category.query.all()
      categories_dict={category.id:category.type for category in categories}

      return jsonify({
        'success':True,
        'categories':categories_dict
      })
    except:
      abort(404)
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions',methods=['GET'])
  def show_questions():
    try:
      questions=Question.query.all()
      categories=Category.query.all()
      
      page_questions=paginations(request, questions)
      categories_dict={category.id:category.type for category in categories}

      return jsonify({
        'success':True,
        'questions':page_questions,
        'total_questions':len(questions),
        'categories':categories_dict
      })
    except:
      abort(404)
  
  #DELETE QUESTION ENDPOINT
  @app.route('/questions/<question_id>',methods=['DELETE'])
  def delete_question(question_id):
    question=Question.query.filter(Question.id==question_id).one_or_none()
    if question is None:
      abort(404)
    try:
      question.delete()
      return jsonify({
        'success':True,
        'deleted':question_id,
        'total_questions':len(Question.query.all())
      })
    except:
      abort(422)
  
  #POST A NEW QUESTION
  @app.route('/questions',methods=['POST'])
  def create_question():
    new_question=request.get_json()
    try:
      question=Question(new_question['question'], new_question['answer'], new_question['category'], new_question['difficulty'])
      existence=Question.query.filter(Question.question==new_question['question']).all()

      if len(existence)!=0: #no repeated questions allowed
        abort(422)
      
      question.insert()
      return jsonify({
        'success':True,
        'created':question.id,
        'total_questions':len(Question.query.all())
      })
    except:
      abort(422)
  
  #GET QUESTIONS BASED ON A SEARCH TERM
  @app.route('/questions/search',methods=['POST'])
  def search_question():
    search_term=request.get_json()['searchTerm']
    results=Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
    if len(results)==0:
      abort(404)
    
    try:
      results=Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
      results_list=[i.format() for i in results]

      return jsonify({
        'success':True,
        'searched':search_term,
        'questions':results_list,
        'total_questions':len(Question.query.all()),
      })
    except:
      abort(400)
  
  #Get Questions by category:
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_categories(category_id):
    category=Category.query.filter(Category.id==category_id).one_or_none()

    if category is None: #category doesnt exist
      abort(404)
    
    category_questions=Question.query.filter(Question.category==category_id).all()
    category_questions_list=[i.format() for i in category_questions]

    if len(category_questions)==0: #no questions for that category
      abort(404)
    
    questions=paginations(request, category_questions)
    
    return jsonify({
      'success':True,
      'category_questions':len(category_questions),
      'questions':category_questions_list,
      'total_questions':len(Question.query.all()),
      'current_category':Category.query.get(category_id).type
    })
  
  #GET POST requests for questions to play the quizz
  @app.route('/quizzes',methods=['POST'])
  def get_question():
    data=request.get_json()
    previous_questions=data['previous_questions']
    quiz_category=data['quiz_category']
    category=Category.query.filter(Category.id==quiz_category['id']).one_or_none()

    if quiz_category['id']==0: #all categories
      try:
        available_questions=Question.query.filter(~Question.id.in_(previous_questions)).all()
        random_question=choice(available_questions).format()

        return jsonify({
          'success':True,
          'question':random_question
        })
      except:
        return jsonify({
          'question':False
        })
    else: #specefic category
      if category is None:
        abort(404)
      try:
        available_category_questions=Question.query.filter(Question.category==quiz_category['id'],~Question.id.in_(previous_questions)).all()
        random_question=choice(available_category_questions).format()
        return jsonify({
          'success':True,
          'question':random_question
        })
      except:
        return jsonify({
          'question':False
        })
  
  #Errors Handlers
  @app.errorhandler(404)
  def not_found_404(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':'resource not found'
    }),404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':'unprocessable'
    }),422
  
  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':400,
      'message':'Bad request'
    }),422

  return app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)