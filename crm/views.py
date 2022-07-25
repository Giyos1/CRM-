from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CourseSerializers, AccountSerializers, PaymentSerializers
from .models import Course, Account, Payment


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


class PaymentAccountView(APIView):
    def get(self, request):
        list_ = []
        course = Course.objects.all()
        course_serializers = CourseSerializers(course, many=True)
        for course in course_serializers.data:
            acoounts = Account.objects.filter(course_id=course['id'])
            acc_serializers = AccountSerializers(acoounts, many=True)
            dict_ = dict(course)
            dict_['accounts'] = acc_serializers.data
            list_.append(dict_)
        return Response(data=list_)

    def post(self, request):
        serializer = PaymentSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class AccountEditView(APIView):
    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        serializer = AccountSerializers(account)
        return Response(data=serializer.data)

    def put(self, request, pk):
        account = Account.objects.get(id=pk)
        serializer = AccountSerializers(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentHistoryView(APIView):
    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        payment = Payment.objects.filter(account=account)
        serializers = PaymentSerializers(payment, many=True)
        return Response(data=serializers.data)
