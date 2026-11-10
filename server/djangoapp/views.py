import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarModel
from .restapis import analyze_review_sentiments, get_request, post_review


def _json_body(request):
    return json.loads(request.body.decode("utf-8") or "{}")


@csrf_exempt
def login_user(request):
    data = _json_body(request)
    username = data.get("userName", "")
    user = authenticate(username=username, password=data.get("password", ""))
    if user is None:
        return JsonResponse({"userName": username, "status": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})


@csrf_exempt
def registration(request):
    data = _json_body(request)
    username = data.get("userName", "").strip()
    password = data.get("password", "")
    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=409)
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=data.get("firstName", ""),
        last_name=data.get("lastName", ""),
        email=data.get("email", ""),
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"}, status=201)


def get_dealerships(request):
    return JsonResponse({"status": 200, "dealers": get_request("fetchDealers")})


def get_dealers_by_state(request, state):
    endpoint = "fetchDealers" if state.lower() == "all" else f"fetchDealers/{state}"
    return JsonResponse({"status": 200, "dealers": get_request(endpoint)})


def get_dealer_details(request, dealer_id):
    return JsonResponse({"status": 200, "dealer": get_request(f"fetchDealer/{dealer_id}")})


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"fetchReviews/dealer/{dealer_id}")
    for review in reviews:
        review["sentiment"] = analyze_review_sentiments(review.get("review", "")).get(
            "sentiment", "neutral"
        )
    return JsonResponse({"status": 200, "reviews": reviews})


def get_cars(request):
    models = list(CarModel.objects.select_related("make").values("make__name", "name", "year"))
    if not models:
        models = [
            {"make__name": "Audi", "name": "A6", "year": 2020},
            {"make__name": "BMW", "name": "X3", "year": 2021},
            {"make__name": "Toyota", "name": "Camry", "year": 2022},
        ]
    return JsonResponse({"CarModels": [
        {"CarMake": item["make__name"], "CarModel": item["name"], "CarYear": item["year"]}
        for item in models
    ]})


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    data = _json_body(request)
    required = ("dealership", "review", "purchase_date", "car_make", "car_model", "car_year")
    if any(not data.get(field) for field in required):
        return JsonResponse({"error": "All review fields are required"}, status=400)
    data["name"] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
    data["dealership"] = int(data["dealership"])
    data["purchase"] = bool(data.get("purchase", True))
    data["car_year"] = int(data["car_year"])
    data["time"] = datetime.utcnow().isoformat()
    review = post_review(data)
    review["sentiment"] = analyze_review_sentiments(review["review"]).get("sentiment", "neutral")
    return JsonResponse({"status": 200, "review": review})


def analyze_review(request, text):
    return JsonResponse(analyze_review_sentiments(text))
