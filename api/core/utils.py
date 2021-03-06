import random
import string
from django.http import JsonResponse
from django.utils.text import slugify


def random_string_generator(
    size=10, chars=string.ascii_lowercase + string.digits
):
    """
    Generates a random string.
    """
    return "".join(random.choice(chars) for _ in range(size))


def slug_generator(instance, new_slug=None):
    """
    Returns a unique slug from the model's ``name`` field if the ``slug``
    query exists in the DB, or the newly created ``slug`` that slugifies the
    model's name if the ``slug`` query does not exist in the DB.

    NOTE: Assumes the instance has a model with ``slug`` and ``name`` fields.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    model = instance.__class__
    query_exists = model.objects.filter(slug=slug).exists()

    if query_exists:
        unique_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )

        # Run this function again to check if the uniquely random slug is
        # truly unique in the DB. If it is unique, return the unique slug.
        # Otherwise, generate another unique slug.
        return slug_generator(instance, new_slug=unique_slug)

    return slug


def error_404(request, exception):
    """
    Custom 404 error response for Django REST Framework.
    """
    response = JsonResponse(
        data={
            "statusCode": 404,
            "status": "fail",
            "message": "The requested URL was not found.",
        }
    )

    return response


def error_500(request):
    """
    Custom 500 error response for Django REST Framework.
    """
    response = JsonResponse(
        data={
            "statusCode": 500,
            "status": "error",
            "message": "Sorry, a technical error has occured.",
        }
    )

    return response


def final_success_response(request, response):
    """
    Custom success response (if no errors i.e. the exception) to change the
    JSON output to have ``statusCode``, ``status``, and ``data``.

    If there is pagination, then its ``metaData`` is put on the same level as
    ``statusCode``, ``status``, and ``data``.

    All of this is done to give a better, clearer, and cleaner JSON output for
    the developers/users.
    """
    if not response.exception:
        response.data = {
            "statusCode": response.status_code,
            "status": "success",
            "data": response.data,
        }

        if (
            "results" in response.data["data"]
            and "metaData" in response.data["data"]
        ):
            pagination_data = response.data["data"].pop("results")
            pagination_meta_data = response.data["data"].pop("metaData")

            response.data["data"] = pagination_data
            response.data["metaData"] = pagination_meta_data


class DictionaryToClass(object):
    """
    A simple class to convert a dictionary into a class. Makes each ``keys``
    into attributes.
    """

    def __init__(self, dictionary: dict[str, any]) -> None:
        if not isinstance(dictionary, dict):
            raise Exception(
                "Needs to be a dictionary of type '<class 'dict'>'."
            )

        if not dictionary:
            raise Exception(
                "A dictionary cannot be empty. Needs to be of type 'dict[str, any]'."
            )

        for key in dictionary:
            setattr(self, key, dictionary[key])
