import openai
from django.http import HttpResponse
from core.settings import OPENAI_API_KEY
from django.views.decorators.http import require_http_methods
from .models import Conversation
from .utils import send_message, logger
from django.views.decorators.csrf import csrf_exempt


# OpenAI API client
openai.api_key = OPENAI_API_KEY

@csrf_exempt
@require_http_methods(["POST"])
def reply(request):
    if request.method == 'POST':
        whatsapp_number = request.POST.get('From', '').split("whatsapp:")[-1]
        print(f"Sending the ChatGPT response to this number: {whatsapp_number}")

        # message content from the request
        body = request.POST.get('Body', '')

        # Call the OpenAI API to generate text with ChatGPT
        messages = [{"role": "user", "content": body}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5
            )

        # The generated text
        chatgpt_response = response.choices[0].message.content

        conversation = Conversation(
            sender=whatsapp_number,
            message=body,
            response=chatgpt_response
            )
        conversation.save()
        logger.info(f"Conversation #{conversation.id} stored in database")
        send_message(whatsapp_number, chatgpt_response)
    return HttpResponse(status=200)

