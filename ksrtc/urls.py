from django.urls import path
from rest_framework.routers import DefaultRouter
from ksrtc.views import KsrtcTripViewSet, UserViewSet

router = DefaultRouter()
router.register(r"ksrtc", KsrtcTripViewSet)
router.register(r"user", UserViewSet)


urlpatterns = router.urls
