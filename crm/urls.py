from django.urls import path
from crm import views

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='List'),
    path('courses/<int:pk>', views.CourseDetail.as_view(), name='Detail'),
    path('payment/', views.PaymentAccountView.as_view(), name='payment')
]
