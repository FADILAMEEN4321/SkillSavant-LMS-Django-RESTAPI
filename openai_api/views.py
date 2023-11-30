from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from openai import OpenAI
from .prompts import assemble_prompt

openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LearningPathCreationApi(APIView):
    def post(self, request):
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
