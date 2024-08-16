from django.urls import path
from .views import UserCreationView,PostView,LikeView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("posts",PostView,basename="posts")
router.register("likes",LikeView,basename="likes")

urlpatterns = [
    path('register/', UserCreationView.as_view(), name='register'),
    path("token/",ObtainAuthToken.as_view(),name="token"),
]+router.urls