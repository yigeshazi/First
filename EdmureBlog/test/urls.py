from django.conf.urls import url
from django.conf.urls import include
from backend.views import user
from web.views import account
urlpatterns = [
    url(r'^tttttt$', account.login),

]
