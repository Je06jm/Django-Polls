from re import M
from django.contrib.auth import authenticate
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import *
from .forms import *

from mysite.utils import get_data, generate_error, generate_success

ERROR_MESSAGE_EXPECTED_JSON = "Expected json"
ERROR_MESSAGE_BAD_REQUEST = "Bad request"
ERROR_MESSAGE_USER_EXIST = "User exist"
ERROR_MESSAGE_NO_SUCH_USER = "No such user"
ERROR_MESSAGE_NO_CHANGES = "No changes to make"
ERROR_MESSAGE_INVALID_CREDENTIALS = "Invalid credentials"
ERROR_MESSAGE_USERNAME_TAKEN = "Username already taken"

SUCCESS_MESSAGE_USER_REGISTERED = "User registered successfully"
SUCCESS_MESSAGE_CHANGES_MADE = "Changes made"
SUCCESS_MESSAGE_USER_DELETED = "User deleted"
SUCCESS_MESSAGE_VALID_LOGIN = "Valid login"


class UserViewSet(viewsets.ViewSet):
    """
    Viewset for User API.
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
        Creates a user.
        """

        # Get header data and verify

        data = get_data(request)

        if not data["username"] or not data["password"]:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # Try to create user
        try:
            user = User.objects.create_user(
                username=data["username"], password=data["password"]
            )

        except:
            return generate_error(ERROR_MESSAGE_USER_EXIST)

        # Save user

        user.save()
        return generate_success(SUCCESS_MESSAGE_USER_REGISTERED)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username", openapi.IN_HEADER, type=openapi.TYPE_STRING, example="John"
            ),
        ],
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "Without <username>": {"users": ["username:string"]},
                        "With <username>": {
                            "date_joined": "date_joined:string",
                            "is_staff": "is_staff:bool",
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
        Lists user information. If no user is specified, then all usernames are returned
        """

        # Get header data and verify

        data = get_data(request)
        user = None

        if data["username"]:
            try:
                user = User.objects.filter(username=data["username"])[0]

            except:
                # No user with "username"
                return generate_error(ERROR_MESSAGE_NO_SUCH_USER)

        if not user:
            # If no "username" is present, then list all usernames
            users = User.objects.all()

            user_data = []
            for user in users:
                user_data += [user.username]

            return generate_success({"users": user_data})

        # Return "username" data

        return generate_success(
            {"date_joined": user.date_joined, "is_staff": user.is_staff}
        )

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
                "new-password",
                openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                example="new password",
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
        Updates the user's password
        """

        # Get header data and verify

        data = get_data(request)

        if not "new-password" in request.headers:
            return generate_error('Missing field "new-password"')

        if not data["username"] or not data["password"]:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        if len(request.headers["new-password"]) == 0:
            return generate_error('"new-password" cannot be empty')

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_NO_SUCH_USER)

        # Update password

        user.set_password(request.headers["new-password"])
        user.save()

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
        Deletes a user
        """

        # Get header data and verify

        data = get_data(request)

        if not data["username"] or not data["password"]:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # See if username and password are valid

        user = authenticate(username=data["username"], password=data["password"])

        if not user:
            return generate_error(ERROR_MESSAGE_INVALID_CREDENTIALS)

        # Delete user

        user.delete()

        return generate_success(SUCCESS_MESSAGE_USER_DELETED)


user_api = UserViewSet.as_view(
    {"post": "create", "get": "list", "put": "update", "delete": "delete"}
)
