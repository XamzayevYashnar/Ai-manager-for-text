from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PagesAi, ChatMessages
from users.models import MainUser
from groq import Groq
from django.conf import settings
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)

@login_required
def home_view(request, page_slug=None):
    page = None
    main_user = MainUser.objects.get(id=request.user.id)

    if page_slug:
        page = PagesAi.objects.filter(slug=page_slug, user=main_user).first()

    if request.method == "POST":
        text_user = request.POST.get('message')

        messages_for_ai = [
            {
                "role": "system", 
                "content": """Siz samimiy AI muharrirsiz. 
                Vazifangiz: foydalanuvchi yuborgan matnni imlo jihatdan tuzatish va uni CHIROYLI, o'qishga qulay formatda qaytarish.
                
                Qoidalar:
                1. Matnni albatta abzaslarga (paragraflarga) bo'ling.
                2. Matnni shunchaki tuzatib qolmay, foydalanuvchi bilan do'stona muloqot qiling.
                3. "Yordamga muhtojligingizga hurmat bering" kabi xato tarjimalarni ishlatmang, sof o'zbek tilida gapiring.
                """
            }
        ]

        if page:
            prev_messages = ChatMessages.objects.filter(chat=page).order_by('created_at')[:10]
            for msg in prev_messages:
                messages_for_ai.append({"role": "user", "content": msg.text_user})
                messages_for_ai.append({"role": "assistant", "content": msg.text_ai})

        messages_for_ai.append({"role": "user", "content": text_user})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=messages_for_ai,      
            max_tokens=1000,
            temperature=0.5,           
        )
        answer_ai = completion.choices[0].message.content

        if not page:
            page = PagesAi.objects.create(
                user=main_user,
                name=text_user[:30] 
            )

        ChatMessages.objects.create(
            user=main_user,
            chat=page,
            text_user=text_user,
            text_ai=answer_ai
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == 'true':
            return JsonResponse({
                'status': 'ok',
                'answer': answer_ai,
                'page_slug': page.slug,
                'page_name': page.name
            })
        
        return redirect('home_detail', page_slug=page.slug)
    
    history = ChatMessages.objects.filter(chat=page).order_by('created_at') if page else []

    context = {
        'page': page,
        'history': history,
        'slug': page_slug
    }
    return render(request, 'home.html', context=context)