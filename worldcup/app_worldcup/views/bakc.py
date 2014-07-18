from django.shortcuts import render_to_response
from app_dbop.models import Guess
import datetime

def worldcup_login(request):
    now = datetime.datetime.now()
    return render_to_response('worldcup_login.html', {'current_date' : now} )


def worldcup_guess(request):
    match1 = request.POST.get('match1', '')
    if match1 == '': 
        return render_to_response('worldcup_guess.html', {"a_path":"images/Brazil.png", "b_path":"images/Croatia.png"}) 
    else:
        return render_to_response('worldcup_guess.html', {"match1":match1, "a_path":"images/Brazil.png", "b_path":"images/Croatia.png"})

