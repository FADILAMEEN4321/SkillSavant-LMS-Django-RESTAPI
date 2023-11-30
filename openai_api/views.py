from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from openai import OpenAI

openAI_client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LearningPathCreationApi(APIView):
    def post(self, request):
        try:
            course = request.data["course"]

            prompt = f"Create a learning path for the course '{course}'. Include relevant topics, resources, and activities. Limit to 50 words. Dont reply to any other questions. Only respond to a valid course name is given. The response should be in bullet point format."

            completion = openAI_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                # temperature=0,
                # max_tokens=2048
                #                  messages=[
                #     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                #     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
                #   ]
            )

            return Response(completion.choices[0].message, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                f"{e}:Error generating learning path",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
