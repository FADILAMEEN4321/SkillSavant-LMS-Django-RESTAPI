from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from openai import OpenAI
from .prompts import assemble_prompt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LearningPathCreationApi(APIView):
    """
    API endpoint for creating a learning path.
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "course": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The course for which the learning path needs to be generated.",
                ),
            },
            required=["course"],
        ),
        responses={
            200: "Successfully generated learning path",
            500: "Internal server error while generating learning path",
        },
    )
    def post(self, request):
        """
        Handle POST requests for creating a learning path.

        :param request: The incoming request object.
        :return: JSON response with the generated learning path or error message.
        """
        try:
            course = request.data["course"]

            messages = assemble_prompt(course)

            completion = openAI_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.2,
                max_tokens=500,
            )

            return Response(completion.choices[0].message, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                f"{e}:Error generating learning path",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )




