from .models import Restaurant, Review
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count

from .forms import LoginForm, RegistrationForm
from .models import Restaurant, Review

def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next'))
            else:
                form.add_error('Invalid credentials!')
    else: # GET
        form = LoginForm()
    return render(request, 'rest_reviews/login.html', {'form': form})


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return redirect(reverse('login'))
    else: # GET
        form = RegistrationForm()
    return render(request, 'rest_reviews/signup.html', {'form': form})


def get_rest_list(request):
    rests = Restaurant.objects.order_by('title')
    # return HttpResponse(
    #     '<ul>'
    #     + ''.join(['<li><a href="/blogger/%s">%s</a></li>' % (b.id, b.title) for b in blogs])
    #     + '</ul>'
    # )
    context = {'restaurants' : rests}
    #template = loader.get_template('blogger/index.html')
    #return HttpResponse(template.render(context, request))

    return render(request, 'rest_reviews/index.html', context)


def restaurant(request, rest_id):
    if request.method == 'POST':
        return create_review(request, rest_id)
    return render_rest(request, rest_id)


def render_rest(request, rest_id, additional_context={}):

    rest = get_object_or_404(Restaurant, id=rest_id)
    

    context = {'rest': rest,
                'reviews': rest.review_set.order_by('-created_at'),
                **additional_context
                }
    #template = loader.get_template('blogger/blog.html')
    #return HttpResponse(template.render(context, request))

    return render(request, 'rest_reviews/restaurant.html', context)


@login_required(login_url='login')
def create_review(request, rest_id):
    rest = get_object_or_404(Restaurant, id=rest_id)

    subject = request.POST['subject']
    subject_error = None
    if not subject or subject.isspace():
        subject_error = 'Please provide non-empty subject!'

    text = request.POST['text']
    text_error = None
    if not text or text.isspace():
        text_error = 'Please provide non-empty text!'

    if subject_error or text_error:
        error_context = {
            'subject_error': subject_error,
            'text_error': text_error,
            'subject': subject,
            'text': text
        }
        return render_rest(request, rest_id, error_context)
    else:
        Review(rest_id=rest.id, subject=subject, text=text).save()
        return HttpResponseRedirect(reverse('rest_by_id', kwargs={'rest_id': rest_id}))