import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}@{}/{}".format('postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question={'question':'What is the biggest country in Africa?',
        'answer':'Algeria',
        'difficulty':1,
        'category':3
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_200_get_categories(self):
        'tests getting all categories in the expected format'
        res=self.client().get('/categories')
        data=json.loads(res.data)
        categories=Category.query.all()
        categories_dict={str(c.id):c.type for c in categories}

        self.assertEqual(200,res.status_code)
        self.assertTrue(data['success'])
        self.assertEqual(dict,type(data['categories']))
        self.assertDictEqual(categories_dict, data['categories'])
    
    def test_404_for_invalid_page(self):
        '''tests if the requested page is beyond valid index'''
        res=self.client().get('/questions?page=9999')
        data=json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'resource not found')
    
    def test_success_paginate_questions(self):
        '''tests if the requested page works fine'''
        res=res=self.client().get('/questions?page=1')
        data=json.loads(res.data)
        questions=Question.query.all()
        categories=Category.query.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], len(questions))
        self.assertEqual(len(data['categories']), len(categories))
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['success'])
    
    def test_200_delete_question(self):
        '''tests if deleting a question works fine'''
        res=self.client().delete('/questions/2')
        data=json.loads(res.data)
        deleted=Question.query.filter(Question.id==2).one_or_none()
        questions=Question.query.all()

        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'],str(2))
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(questions),data['total_questions'])
    
    def test_404_cant_delete_unexisted_question(self):
        '''tests if the requested question does not exist'''
        res=self.client().delete('/questions/9999')
        data=json.loads(res.data)
        question=Question.query.filter(Question.id==9999).one_or_none()

        self.assertEqual(res.status_code,404)
        self.assertEqual(question,None)
        self.assertEqual(data['message'],'resource not found')
        self.assertFalse(data['success'])
    
    def test_404_search_question_not_found(self):
        '''tests if the searched question(s) doesnt exist'''
        res=self.client().post('/questions/search', json={'searchTerm':'you cant find me'})
        data=json.loads(res.data)
        searched=Question.query.filter(Question.question.ilike('%'+'you cant find me'+'%')).all()

        self.assertEqual(res.status_code,404)
        self.assertEqual(len(searched),0)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'resource not found')
    
    def test_200_search_question(self):
        '''tests if searching for questions by term works fine'''

        res=self.client().post('/questions/search', json={'searchTerm':'egypt'})
        data=json.loads(res.data)
        searched=Question.query.filter(Question.question.ilike('%'+'egypt'+'%')).all()
        searched_list=[i.format() for i in searched]

        self.assertEqual(res.status_code, 200)
        self.assertListEqual(searched_list, data['questions'])
        self.assertTrue(data['success'])
        self.assertGreater(len(searched), 0)
    
    def test_200_add_question(self):
        '''tests if adding a new question works fine '''
        
        res=self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)
        added_to_db=Question.query.filter(Question.question==self.new_question['question']).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertNotEqual(added_to_db,None)
        self.assertEqual(data['created'],added_to_db.id)
        self.assertTrue(data['success'])
    
    def test_422_no_repeated_questions_allowed(self):
        ''' tests if adding an existing question is unprocessable'''
        res=self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)
        existed=Question.query.filter(Question.question==self.new_question['question']).all()

        self.assertEqual(res.status_code,422)
        self.assertFalse(data['success'])
        self.assertEqual(1,len(existed))
    
    def test_404_category_doesnt_exist(self):
        '''tests getting a non existing category's questions'''

        res=self.client().get('/categories/99/questions')
        data=json.loads(res.data)
        category=Category.query.filter(Category.id==99).all()

        self.assertEqual(res.status_code,404)
        self.assertEqual(len(category),0)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'],'resource not found')
    
    def test_200_get_questions_by_category(self):
        '''tests getting questions by category'''
        res=self.client().get('/categories/1/questions')
        questions=Question.query.filter(Question.category==1).all()
        category_questions=[i.format() for i in questions]
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['current_category'],'Science')
        self.assertListEqual(data['category_questions'], category_questions)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'],len(Question.query.all()))
    
    def test_404_quizz_category_not_found(self):
        '''tests if selected quizz category doesnt exist'''
        quizz_data={
            "previous_questions":[3],
            "quiz_category":{'type':'NO','id':55}
        }
        res=self.client().post('/quizzes',json=quizz_data)
        data=json.loads(res.data)
        category=Category.query.filter(Category.id==55).one_or_none()

        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])
        self.assertEqual(category,None)
    
    def test_200_quizz(self):
        '''tests if the quizz renders the expected behaviour'''
        quizz_data={
            "previous_questions":[10],
            "quiz_category":{'type':'Sports','id':6}
        }
        res=self.client().post('/quizzes',json=quizz_data)
        data=json.loads(res.data)
        next_question=Question.query.filter(Question.question==data['question']['question']).one_or_none()

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code,200)
        self.assertNotEqual(None,next_question)
    
    def test_quizz_no_available_questions(self):
        '''tests if there is no more category questions available'''
        quizz_data={
            "previous_questions":[10,11],
            "quiz_category":{'type':'Sports','id':6}
        }
        res=self.client().post('/quizzes',json=quizz_data)
        data=json.loads(res.data)
        next_question=Question.query.filter(Question.category==6).all() #category questions

        self.assertEqual(len(next_question),len(quizz_data['previous_questions'])) 
        self.assertEqual(False,data['question'])
    








# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()