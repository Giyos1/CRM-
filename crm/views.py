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
        course_serializers = CourseSerializers(course)
        account = Account.nodeleted.filter(course=course)
        acc_serializers = AccountSerializers(account, many=True)
        for acc in acc_serializers.data:
            account = Account.nodeleted.get(id=acc['id'])
            payment = account.payment.all()
            pay_serializers = PaymentSerializers(payment, many=True)
            a_serializers = AccountSerializers(account)
            dict_ = dict(a_serializers.data)
            dict_['payment'] = pay_serializers.data
            list_.append(dict_)
        co = dict(course_serializers.data)
        co["account"] = list_
        return Response(data=co)


class PaymentAccountView(APIView):
    def get(self, request):
        list_ = []
        course = Course.objects.all()
        course_serializers = CourseSerializers(course, many=True)
        for course in course_serializers.data:
            acoounts = Account.nodeleted.filter(course_id=course['id'])
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
        account = Account.nodeleted.get(id=pk)
        serializer = AccountSerializers(account)
        return Response(data=serializer.data)

    def put(self, request, pk):
        account = Account.nodeleted.get(id=pk)
        serializer = AccountSerializers(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentHistoryView(APIView):
    def get(self, request, pk):
        account = Account.nodeleted.get(id=pk)
        payment = Payment.objects.filter(account=account)
        serializers = PaymentSerializers(payment, many=True)
        return Response(data=serializers.data)


class PaymentEditView(APIView):
    def get(self, request, pk):
        payment = Payment.objects.get(id=pk)
        serializers = PaymentSerializers(payment)
        return Response(data=serializers.data)

    def put(self, request, pk):
        payment = Payment.objects.get(id=pk)
        serializer = PaymentSerializers(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnknownAccountView(APIView):
    def get(self, request):
        list_ = []
        course = Course.objects.filter()
        course_serializers = CourseSerializers(course, many=True)
        print(course_serializers.data)

        for course in course_serializers.data:
            acoounts = Account.nodeleted.filter(course_id=course['id'], first_name__contains='unknown',
                                                last_name__contains='unknown', phone_number__contains='unknown')
            acc_serializers = AccountSerializers(acoounts, many=True)
            dict_ = dict(course)
            dict_['unknown_count'] = acoounts.count()
            dict_['accounts'] = acc_serializers.data
            list_.append(dict_)
        return Response(data=list_)


class CourseLeaveView(APIView):
    def get(self, request):
        list_ = []
        courses = Course.objects.all()
        serializers = CourseSerializers(courses, many=True)
        for i in serializers.data:
            number = Account.nodeleted.filter(course_id=i['id']).count()
            number -= i['number_student']
            dict_ = dict(i)
            dict_['leave_account'] = number
            list_.append(dict_)
        return Response(data=list_)


class SwappingCourseAccountView(APIView):
    def get(self, request, pk):
        courses = Course.objects.all()
        serializers = CourseSerializers(courses, many=True)
        return Response(data=serializers.data)

    def put(self, request, pk):
        account = Account.nodeleted.get(id=pk)
        serializer = AccountSerializers(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):

    def get(self, request, pk):
        account = Account.nodeleted.get(id=pk)
        serializer = AccountSerializers(account)
        return Response(data=serializer.data)

    def put(self, request, pk):
        account = Account.nodeleted.get(id=pk)
        serializer = AccountSerializers(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountListView(APIView):
    def get(self, request):
        list_ = []
        courses = Course.objects.all()
        serializers = CourseSerializers(courses, many=True)
        for i in serializers.data:
            accounts = Account.objects.filter(course_id=i['id'], delete=True)
            acc_serializers = AccountSerializers(accounts, many=True)
            dict_ = dict(i)
            dict_['accounts'] = acc_serializers.data
            list_.append(dict_)
        return Response(data=list_)


class AccountCountView(APIView):
    def get(self):
        pass
