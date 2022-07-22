from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CourseSerializers, AccountSerializers, PaymentSerializers
from .models import Course, Account


class CourseList(ListAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()


class CourseDetail(APIView):
    def get(self, request, pk):
        list_ = []
        course = Course.objects.get(id=pk)
        account = Account.objects.filter(course=course)
        acc_serializers = AccountSerializers(account, many=True)
        for acc in acc_serializers.data:
            account = Account.objects.get(id=acc['id'])
            payment = account.payment.all()
            pay_serializers = PaymentSerializers(payment, many=True)
            a_serializers = AccountSerializers(account)
            dict_ = dict(a_serializers.data)
            dict_['payment'] = pay_serializers.data
            list_.append(dict_)

        return Response(data=list_)
