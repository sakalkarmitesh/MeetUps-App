from django.shortcuts import render, redirect
from .models import Meetup, Participant
from .forms import RegistrationForm
from django.http import HttpResponse


# Create your views here.

# index function is defined, which serves as the view for a particular URL.
# In Django, a view is a Python function that receives an HTTP request and returns an HTTP response.


def index(request):
    meetups = Meetup.objects.all()
    # meetups = [
    #     {'title': 'A first Meetup',
    #      'location': 'New York',
    #      'slug': 'a-first-meetup'
    #     },
    #     {'title': 'A second Meetup',
    #      'location': 'Paris',
    #      'slug': 'a-second-meetup'
    #      }
    # ]
    return render(request, 'meetups/index.html', {
        'meetups': meetups
    })


def meetup_details(request, meetup_slug):
    try:
        selected_meetup = Meetup.objects.get(slug=meetup_slug)
        if request.method == 'GET':
            registration_form = RegistrationForm()

            # selected_meetup = {
            #     'title': 'A First Meetup',
            #     'description': 'This is the first meetup!'
            # }

        else:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                user_email = registration_form.cleaned_data['email']
                participant, _ = Participant.objects.get_or_create(email=user_email)
                selected_meetup.participant.add(participant)
                return redirect('confirm-registration', meetup_slug=meetup_slug)

        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': True,
            'selected_title': selected_meetup,
            'form': registration_form
        })

    except Exception as exc:
        print(exc)
        return render(request, 'meetups/meetup-details.html', {
            'meetup_found': False
        })


def confirm_registration(request, meetup_slug):
    return render(request, 'meetups/registration-success.html')

# Inside the index function, a HttpResponse object is created. This object represents the HTTP response
# that will be sent back to the user's browser. In this case, the response contains the string 'Hello World'.
