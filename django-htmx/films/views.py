from typing import Any

from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from films.models import Film
from django.views.generic.list import ListView
from django.contrib import messages

from films.forms import RegisterForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class Login(LoginView):
    template_name = "registration/login.html"


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class FilmList(LoginRequiredMixin, ListView):
    template_name = "films.html"
    model = Film
    context_object_name = "films"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        return user.films.all()


def check_username(request: HttpRequest):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse(
            "<div id='username-error' class='error'>Username already exists!</div>"
        )
    else:
        return HttpResponse(
            "<div id='username-error' class='success'>Username available!</div>"
        )


@login_required
def add_film(request: HttpRequest):
    name = request.POST.get("filmname")

    film = Film.objects.get_or_create(name=name)[0]
    request.user.films.add(film)

    context = {"films": request.user.films.all()}
    messages.success(request, f"Added {name} to films!")
    return render(request, "partials/film-list.html", context=context)


@login_required
@require_http_methods(["DELETE"])
def delete_film(request: HttpRequest, pk):
    request.user.films.remove(pk)
    context = {"films": request.user.films.all()}
    return render(request, "partials/film-list.html", context=context)


def search_films(request: HttpRequest):
    search_text = request.POST.get("search")
    results = Film.objects.filter(name__icontains=search_text)  # Case insensitive match
    context = {"results": results}
    return render(request, "partials/search-results.html", context=context)

def clear(request: HttpRequest):
    return HttpResponse("")