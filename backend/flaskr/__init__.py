
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @OK: Set up CORS. Allow '*' for origins.
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @OK: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @OK:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    # CATEGORIES 
    @app.route('/categories', methods=["GET"])
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)
        data = {}
        for cat in categories:
            data[cat.id] = cat.type
        return jsonify(
            {
                "categories": data
            }
        )

    """
    @OK:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    # QUESTIONS 
    @app.route("/questions")
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        categories = Category.query.order_by(Category.id).all()
        categories_data = {}
        for cat in categories:
            categories_data[cat.id] = cat.type
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(Question.query.all()),
                "categories": categories_data,
                "currentCategory": "History"
            }
        )
    """
    @OK:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                                            Question.id == question_id
                                            ).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except Exception as e:
            print(e)
            abort(422)

    """
    @OK:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question
    will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @OK:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
        new_question = body.get("question", None)
        
        search_term = body.get("searchTerm", None)

        try:
            if search_term:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))
                )
                current_questions = paginate_questions(request, selection)
                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": len(selection.all()),
                        "currentCategory": "History"
                    }
                )
            else:
                question = Question(
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty,
                    question=new_question
                    )
                question.insert()

                return jsonify(
                    {
                        "success": True
                    }
                )

        except Exception as e:
            print(e)
            abort(422)
    """
    @OK:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:cat_id>/questions")
    def retrieve_questions_per_category(cat_id):
        selection = Question.query.filter_by(category=cat_id).all()
        category = Category.query.filter_by(id=cat_id).one_or_none()
        if selection is None:
            abort(404)
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        return jsonify(
            {
                "questions": current_questions,
                "totalQuestions": len(Question.query.all()),
                "currentCategory": category.type
            }
        )
    """
    @OK:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=['POST'])
    def display_quizzes():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        current_category_json = body.get("quiz_category", None)
        if type(current_category_json) is str:
            current_category = current_category_json
        else:
            current_category = current_category_json.get("type", None)
        num_question_per_cat = 0
        if current_category == 'click':
            filtered_quizz = Question.query.filter(
                                    Question.id.notin_(previous_questions)
                                                    ).all()
            questions_id = [question.id for question in filtered_quizz]
            if questions_id == []:
                quizzid = 0
            else:
                quizzid = random.choice(questions_id)
            new_quizz = Question.query.filter_by(id=quizzid).one_or_none()
            num_question_per_cat = Question.query.count()
        else:
            current_category_info = Category.query.filter_by(
                                        type=current_category
                                                            ).one()
            filtered_quizz = Question.query.filter(
                                Question.category == current_category_info.id,
                                Question.id.notin_(
                                            previous_questions
                                            )
                                            ).all()
            questions_id = [question.id for question in filtered_quizz]
            if questions_id == []:
                quizzid = 0
            else:
                quizzid = random.choice(questions_id)
            new_quizz = Question.query.filter_by(id=quizzid).one_or_none()
            num_question_per_cat = Question.query.filter(
                                    Question.category ==
                                    current_category_info.id
                                    ).count()

        if new_quizz is None:
            return jsonify(
                {
                    "question": "end"
                }
            )
        else:
            return jsonify(
                {
                    "question": new_quizz.format(),
                    "num_question_per_cat": num_question_per_cat
                }
            )
    """
    @OK:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
            ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
            ), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed"
            }
            ), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }
            ), 422

    return app
