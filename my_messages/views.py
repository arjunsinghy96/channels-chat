from django.shortcuts import render, redirect
from my_messages.models import League

def home_page(request):
    if request.method == 'POST':
        room = request.POST['room']
        username = request.POST['username']
        request.session['username'] = username
        return redirect('chat', permanent=True, room=room)
    return render(request, 'home.html')

def chat_page(request, room):
    league, created  = League.objects.get_or_create(name='chat-%s'%room)
    messages = league.messages.all().order_by('-timestamp')
    return render(request, 'chat.html',
            {
                'username': request.session['username'],
                'messages': messages,
            }
        )
