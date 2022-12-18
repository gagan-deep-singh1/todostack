from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as DjangoUser
from django.shortcuts import render, redirect
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView

from accounts.forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import User


class RegistrationView(APIView):
    parser_classes = [JSONParser, FormParser]
    def get(self, request):
        form = RegisterForm()
        context_data = {"form": form, "title": "Register"}
        return render(request, "accounts/register.html", context_data)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("first_name")
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Hey {name}, Your account has been created successfully. You can login now.",
            )

            return redirect("login")

        return render(
            request, "accounts/register.html", {"form": form, "title": "Register"}
        )


class AccountsView(APIView, LoginRequiredMixin):
    parser_classes = [JSONParser, FormParser]
    def get(self, request):
        current_user = request.user
        fname = DjangoUser.objects.filter(username=current_user).first().first_name
        lname = DjangoUser.objects.filter(username=current_user).first().last_name
        context = {
            "title": current_user,
            "name": fname + " " + lname,
        }

        return render(request, "accounts/accounts.html", context)


class EditAccountsView(APIView, LoginRequiredMixin):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        user = User.objects.get(system_user_id=request.user.id)
        profile_form = ProfileUpdateForm(instance=user)

        context = {"u_form": user_form, "p_form": profile_form, "title": "Edit Account"}

        return render(request, "accounts/edit_accounts.html", context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        user = User.objects.get(system_user_id=request.user.id)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(
                request, messages.INFO, f"Your details have been saved successfully."
            )
            return redirect("profile")

        return render(
            request,
            "accounts/edit_accounts.html",
            {"u_form": user_form, "p_form": profile_form, "title": "Edit Account"},
        )
