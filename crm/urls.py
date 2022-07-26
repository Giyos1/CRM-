from django.urls import path
from crm import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'botcourse', views.CourseViewSetForBot)

urlpatterns = [
                  path('courses/', views.CourseActiveList.as_view(), name='List'),
                  path('stoppedcourse/', views.CourseNoActiveList.as_view(), name='noactive'),
                  path('courses/<int:pk>/edit/', views.CourseEditView.as_view(), name='List'),
                  path('courses/<int:pk>/', views.CourseDetail.as_view(), name='Detail'),
                  path('account/<int:pk>/edit/', views.AccountEditView.as_view(), name='edit'),
                  path('account/<int:pk>/paymenthistory/', views.PaymentHistoryView.as_view(), name='paymenthistory'),
                  path('payment/<int:pk>/edit/', views.PaymentEditView.as_view(), name='payment-edit'),
                  path('payment/', views.PaymentAccountView.as_view(), name='payment'),
                  path('unknownaccount/', views.UnknownAccountView.as_view(), name='unknown'),
                  path('leaveaccount/', views.CourseLeaveView.as_view(), name='leave-account'),

                  path('swapping/account/<int:pk>/', views.SwappingCourseAccountView.as_view(), name='swapping'),
                  path('delete/account/<int:pk>/', views.DeleteAccountView.as_view(), name='delete'),
                  path('deleteaccountlist/', views.DeleteAccountListView.as_view(), name='delete-list'),
                  path('generalpaymenthistory/', views.GeneralPaymentHistory.as_view(), name='paymenthistory'),
                  path('statusapi/', views.AccountCountView.as_view(), name='status'),
                  path('payment/<int:pk>/deleteaccount/', views.PaymentDeleteAccountView.as_view(), name='pay'),

              ] + router.urls
