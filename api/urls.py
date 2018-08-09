

from django.conf.urls import url
from api.views import course
from api.views import shoppingcar


urlpatterns = [
    url(r'^courses/$', course.CoursesView.as_view()),
    url(r'^courseprice/$', course.CoursesPrice.as_view()),
    url(r'^shoppingcar/$', shoppingcar.ShoppingCarView.as_view({'post':'create','get':'list','delete':'destroy','put':'update'})),
]
