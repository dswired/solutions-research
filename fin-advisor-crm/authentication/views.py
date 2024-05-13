from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth, messages


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    msg = f"Welcome {user.first_name}, you are now logged in!"
                    messages.success(request, msg)
                    return redirect("main-monitor")
                msg = "The account you entered is not active please see your administrator."
                messages.error(request, msg)
                return render(request, "authentication/login.html")
            msg = "The account you entered is not active please see your administrator."
            messages.error(request, msg)
            return render(request, "authentication/login.html")
        messages.error(request, "Missing credentials. Please fill in all fields")
        return render(request, "authentication/login.html")

class LogOutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out!")
        return redirect('login')
