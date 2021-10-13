from secrets import choice
from pkg_resources import require
from rest_framework import viewsets
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.views import ERROR_MESSAGE_NO_SUCH_USER

from .models import *
from mysite.utils import get_data, generate_error, generate_success

import json

ERROR_MESSAGE_EXPECTED_JSON = "Expected json"
ERROR_MESSAGE_BAD_REQUEST = "Bad request"
ERROR_MESSAGE_NO_CHANGES = "No changes to make"
ERROR_MESSAGE_INVALID_CREDENTIALS = "Invalid credentials"
ERROR_MESSAGE_QUESTION_EXIST = "Question exist"
ERROR_MESSAGE_NO_QUESTION = "Question does not exist"
ERROR_MESSAGE_ALREADY_VOTED = "Already voted"
ERROR_MESSAGE_NO_OPTION = "No option provided"
ERROR_MESSAGE_NOT_PERMITTED = "User is not permitted"

SUCCESS_MESSAGE_QUESTION_CREATED = "Question created"
SUCCESS_MESSAGE_CHANGES_MADE = "Changes made"
SUCCESS_MESSAGE_QUESTION_DELETED = "Question deleted"
SUCCESS_MESSAGE_VOTED = "Voted"
SUCCESS_MESSAGE_DELETED_VOTE = "Deleted vote"


class QuestionViewSet(viewsets.ViewSet):
    """
    ViewSet for Question API.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="John",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="password",
            ),
            openapi.Parameter(
                "text",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="Here's a question",
            ),
            openapi.Parameter(
                "options",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="a,b",
                description="Values are comma seperated",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={"application/json": {"message": "success_message:string"}},
            ),
            400: openapi.Response(
                description="Error", examples={"text/html": "error_message"}
            ),
        },
    )
    def create(self, request):
        """
        Creates a question.
        """

        # Get header data and verify

        data = get_data(request)

        if not data["username"] or not data["password"]:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        if not "text" in request.headers or len(request.headers["text"]) == 0:
            return generate_error('Expected field "text"')

        if not "options" in request.headers or len(request.headers["options"]) == 0:
            return generate_error('Expected field "options"')

        text = request.headers["text"]
        options = request.headers["options"].split(",")

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_NO_SUCH_USER)

        # Generate question

        q = Question(text=text, user=user)
        q.save()

        for option in options:
            o = Option(text=option, question=q)
            o.save()

        return generate_success(SUCCESS_MESSAGE_QUESTION_CREATED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "question", openapi.IN_HEADER, type=openapi.TYPE_INTEGER, required=False
            )
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "Without <question>": {
                            "questions": {"question_id:int": "question_text:string"}
                        },
                        "With <question>": {
                            "user": "username:string",
                            "text": "question_text:string",
                            "options": {
                                "option_id:int": {
                                    "text": "option_text:string",
                                    "votes": "option_votes:int",
                                }
                            },
                            "publish date": "publish_date:string",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Error", examples={"text/html": "error_message"}
            ),
        },
    )
    def list(self, request):
        """
        Lists all questions. If a question is provided, then the information about it will be listed
        """

        # Get header data and verify

        data = get_data(request)
        q = None

        # If "question" is specified, then see if it's a real question
        if "question" in request.headers:
            try:
                q = Question.objects.filter(pk=int(request.headers["question"]))[0]

            except:
                return generate_error(ERROR_MESSAGE_NO_QUESTION)

        # If no "question" is specified, then list all of the questions along with their IDs
        if not q:
            questions = Question.objects.all()

            question_data = {}
            for question in questions:
                question_data.update({question.pk: question.text})

            return generate_success({"questions": question_data})

        # Return "question" data
        data = {
            "user": q.user.username,
            "text": q.text,
            "options": {},
            "publish date": q.pub_date,
        }

        options = Option.objects.filter(question=q)
        for option in options:
            votes = len(Vote.objects.filter(option=option))
            data["options"].update(
                {str(option.pk): {"text": option.text, "votes": votes}}
            )

        return generate_success(data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="John",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="password",
            ),
            openapi.Parameter(
                "question", openapi.IN_HEADER, type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                "new-text",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="New question text",
            ),
            openapi.Parameter(
                "new-options",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="New Option,Rename This->To That,Delete This->",
                description='Values are comma seperated. Items without "->" are added as new options. Items with "->" are renamed to the right side if not empty, deleted otherwise',
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={"application/json": {"message": "success_message:string"}},
            ),
            400: openapi.Response(
                description="Error", examples={"text/html": "error_message"}
            ),
        },
    )
    def update(self, request):
        """
        Updates question.
        """

        # Get header data and verify

        data = get_data(request)

        if not "question" in request.headers:
            return generate_error('Expected field "question"')

        if not data["username"] or not data["password"]:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # Get "question"

        try:
            q = Question.objects.filter(pk=int(request.headers["question"]))[0]

        except:
            return generate_error(ERROR_MESSAGE_NO_QUESTION)

        if not user == q.user:
            return generate_error(ERROR_MESSAGE_NOT_PERMITTED)

        # Update "question" data

        if "new-text" in request.headers and len(request.headers["new-text"]) != 0:
            q.text = request.headers["new-text"]

        if "new-options" in request.headers:
            options = request.headers["new-options"].split(",")

            for option in options:
                if option.find("->") != -1:
                    option = option.split("->")

                    try:
                        o = Option.objects.filter(question=q, text=option[0])[0]

                    except Exception as e:
                        return generate_error(
                            "Option " + option[0] + " is not an option"
                        )

                    if len(option) == 2 and option[1] != "":
                        o.text = option[1]
                        o.save()

                    else:
                        o.delete()

                else:
                    o = Option(question=q, text=option)
                    o.save()

        q.save()
        return generate_success(SUCCESS_MESSAGE_CHANGES_MADE)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="John",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="password",
            ),
            openapi.Parameter(
                "question", openapi.IN_HEADER, type=openapi.TYPE_INTEGER, required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={"application/json": {"message": "success_message:string"}},
            ),
            400: openapi.Response(
                description="Error", examples={"text/html": "error_message"}
            ),
        },
    )
    def delete(self, request):
        """
        Deletes a post.
        """

        # Get header data and verify

        data = get_data(request)

        if not "question" in request.headers:
            return generate_error('Expected field "question"')

        if not data["username"] or not data["password"]:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        try:
            q = Question.objects.filter(pk=int(request.headers["question"]))[0]

        except:
            return generate_error(ERROR_MESSAGE_NO_QUESTION)

        if not user == q.user:
            return generate_error(ERROR_MESSAGE_NOT_PERMITTED)

        # Delete question

        q.delete()
        return generate_success(SUCCESS_MESSAGE_QUESTION_DELETED)


class VoteViewSet(viewsets.ViewSet):
    """
    ViewSet for Vote
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="John",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="password",
            ),
            openapi.Parameter(
                "question", openapi.IN_HEADER, type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                "options",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="1,2",
                description="Values are comma seperated",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={"application/json": {"message": "success_message:string"}},
            ),
            400: openapi.Response(
                description="Error", examples={"text/html": "error_message"}
            ),
        },
    )
    def vote(self, request):
        """
        Records a vote.
        """

        # Get header data and verify

        data = get_data(request)

        if not "question" in request.headers:
            return generate_error('Expected field "question"')

        if not "options" in request.headers:
            return generate_error('Expected field "options"')

        try:
            q = Question.objects.filter(pk=int(request.headers["question"]))[0]

        except:
            return generate_error(ERROR_MESSAGE_NO_QUESTION)

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # Record votes for options

        options = request.headers["options"].split(",")

        for option in options:
            try:
                o = Option.objects.filter(pk=option, question=q)[0]

            except:
                return generate_error(ERROR_MESSAGE_NO_OPTION)

            try:
                v = Vote.objects.filter(user=user, option=o)[0]

            except:
                v = None

            if v:
                return generate_error(ERROR_MESSAGE_ALREADY_VOTED)

            v = Vote(user=user, option=o)
            v.save()

        return generate_success(SUCCESS_MESSAGE_VOTED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="John",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="password",
            ),
            openapi.Parameter(
                "question", openapi.IN_HEADER, type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                "options",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="1,2",
                description="Values are comma seperated",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={"application/json": {"message": "success_message:string"}},
            ),
            400: openapi.Response(
                description="Error", examples={"text/html": "error_message"}
            ),
        },
    )
    def delete(self, request):
        """
        Deletes one or more votes.
        """

        # Get header data and verify

        data = get_data(request)

        if not "question" in request.headers:
            return generate_error('Expected field "question"')

        try:
            q = Question.objects.filter(pk=int(request.headers["question"]))[0]

        except:
            return generate_error(ERROR_MESSAGE_NO_QUESTION)

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        options = []

        if "options" in request.headers:
            options = request.headers["options"].split(",")

        if len(options) == 0:
            # Delete all votes
            try:
                o = Option.objects.filter(question=q)

                for option in o:
                    options += [option.pk]

            except:
                return generate_error("Question has no options")

        # Delete votes for specified options

        for option in options:
            try:
                o = Option.objects.filter(pk=option, question=q)[0]

            except:
                return generate_error(ERROR_MESSAGE_NO_OPTION)

            try:
                v = Vote.objects.filter(user=user, option=o)[0]

            except:
                continue

            v.delete()

        return generate_success(SUCCESS_MESSAGE_DELETED_VOTE)


question_api = QuestionViewSet.as_view(
    {"post": "create", "get": "list", "put": "update", "delete": "delete"}
)

vote_api = VoteViewSet.as_view({"post": "vote", "delete": "delete"})
