import json
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body or "{}")
    username = data.get("userName", "")
    user = authenticate(username=username, password=data.get("password", ""))
    response = {"userName": username, "status": "Invalid credentials"}
    if user is not None:
        login(request, user)
        response["status"] = "Authenticated"
    return JsonResponse(response)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body or "{}")
    username = data.get("userName", "")
    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )
    user = User.objects.create_user(
        username=username,
        first_name=data.get("firstName", ""),
        last_name=data.get("lastName", ""),
        email=data.get("email", ""),
        password=data.get("password", ""),
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"})


def get_cars(request):
    if not CarMake.objects.exists():
        initiate()
    car_models = [
        {
            "CarMake": model.car_make.name,
            "CarModel": model.name,
            "CarType": model.type,
            "CarYear": model.year,
            "DealerId": model.dealer_id,
        }
        for model in CarModel.objects.select_related("car_make")
    ]
    return JsonResponse({"CarModels": car_models, "status": 200})


def get_dealerships(request, state=None):
    endpoint = "/fetchDealers" if state is None else f"/fetchDealers/{state}"
    return JsonResponse({"dealers": get_request(endpoint), "status": 200})


def get_dealer_details(request, dealer_id):
    return JsonResponse(
        {"dealer": get_request(f"/fetchDealer/{dealer_id}"), "status": 200}
    )


def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
    for review in reviews:
        sentiment = analyze_review_sentiments(review.get("review", ""))
        review["sentiment"] = sentiment.get("sentiment", sentiment)
    return JsonResponse({"reviews": reviews, "status": 200})


@csrf_exempt
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    data = json.loads(request.body or "{}")
    return JsonResponse({"review": post_review(data), "status": 200})
