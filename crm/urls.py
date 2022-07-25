from django.urls import path
from crm import views

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='List'),
    path('courses/<int:pk>', views.CourseDetail.as_view(), name='Detail'),
    path('payment/', views.PaymentAccountView.as_view(), name='payment'),
    path('account/<int:pk>/edit/', views.AccountEditView.as_view(), name='edit'),
    path('account/<int:pk>/paymenthistory/', views.PaymentHistoryView.as_view(), name='paymenthistory'),

]
