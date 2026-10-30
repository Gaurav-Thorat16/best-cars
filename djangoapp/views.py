import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods


def _json_body(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return None


def home(request):
    dealers = [
        {"state": "California", "name": "Best Cars Downtown", "address": "2400 Market Street", "city": "San Francisco", "zip": "94114"},
        {"state": "California", "name": "Best Cars Peninsula", "address": "1800 El Camino Real", "city": "San Mateo", "zip": "94404"},
        {"state": "Kansas", "name": "Best Cars Wichita", "address": "515 North Market Street", "city": "Wichita", "zip": "67202"},
    ]
    selected_state = request.GET.get("state", "").strip()
    filtered_dealers = [dealer for dealer in dealers if not selected_state or dealer["state"].lower() == selected_state.lower()]
    states = sorted({dealer["state"] for dealer in dealers})
    return render(request, "djangoapp/home.html", {"dealers": filtered_dealers, "states": states, "selected_state": selected_state})


def about(request):
    return render(request, "djangoapp/about.html")


def contact(request):
    return render(request, "djangoapp/contact.html")


@ensure_csrf_cookie
def login_page(request):
    return render(request, "djangoapp/login.html")


@ensure_csrf_cookie
def register_page(request):
    return render(request, "djangoapp/register.html")


@require_http_methods(["POST"])
def login_api(request):
    data = _json_body(request)
    if not data or not data.get("username") or not data.get("password"):
        return JsonResponse({"error": "Username and password are required."}, status=400)

    user = authenticate(
        request,
        username=data["username"].strip(),
        password=data["password"],
    )
    if user is None:
        return JsonResponse({"error": "Invalid username or password."}, status=401)

    login(request, user)
    return JsonResponse({"authenticated": True, "username": user.username})


@require_http_methods(["POST"])
def register_api(request):
    data = _json_body(request)
    username = data.get("username", "").strip() if data else ""
    password = data.get("password", "") if data else ""

    if not username or not password:
        return JsonResponse({"error": "Username and password are required."}, status=400)
    if len(password) < 8:
        return JsonResponse({"error": "Password must be at least 8 characters."}, status=400)
    if User.objects.filter(username__iexact=username).exists():
        return JsonResponse({"error": "That username is already registered."}, status=409)

    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    return JsonResponse({"authenticated": True, "username": user.username}, status=201)


@require_http_methods(["POST"])
def logout_api(request):
    logout(request)
    return JsonResponse({"authenticated": False})
