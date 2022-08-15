from rest_framework import status, viewsets, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CourseSerializers, AccountSerializers, PaymentSerializers
from .models import Course, Account, Payment


class CourseActiveList(ListAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = Course.objects.filter(is_active=True)

        return queryset


class CourseNoActiveList(ListAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = Course.objects.filter(is_active=False)

        return queryset


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
        account = Account.objects.get(id=pk)
        c_id = request.data['course']
        course = Course.objects.get(id=c_id)
        if course.active_month < account.start_course:
            request.data['start_course'] = course.active_month

        serializer = AccountSerializers(account, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):

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


class DeleteAccountListView(APIView):
    def get(self, request):
        list_ = []
        courses = Course.objects.all()
        serializers = CourseSerializers(courses, many=True)
        for i in serializers.data:
            acc_list = []
            dict_ = dict(i)
            accounts = Account.objects.filter(course_id=i['id'], delete=True)
            acc_serializers = AccountSerializers(accounts, many=True)
            for p in acc_serializers.data:
                acc = Account.objects.get(id=p['id'])
                p['umumiy summasi'] = acc.payments
                p['qarzi'] = acc.delete_qarzdorlik
                acc_list.append(p)
            dict_['accounts'] = acc_list

            list_.append(dict_)
        return Response(data=list_)


class AccountCountView(APIView):
    def get(self, request):
        data = {}
        qarzdorlik_summasi = 0
        ota_qardorlar = []
        qarzdorlar = []
        account_number = Account.nodeleted.exclude(first_name__contains='unknown', last_name__contains='unknown',
                                                   phone_number__contains='unknown').count()
        accounts = Account.objects.exclude(first_name__contains='unknown', last_name__contains='unknown',
                                           phone_number__contains='unknown')
        delete_account_number = Account.objects.filter(delete=True).count()
        for acc in accounts:
            if not acc.delete:
                if acc.qarzdorlik > 0 and acc.qarzdorlik - acc.oquvchi_narxi > 0:
                    qarzdorlik_summasi += acc.qarzdorlik
                    seria = AccountSerializers(acc)
                    dict_ = dict(seria.data)
                    dict_['qarzi'] = acc.qarzdorlik
                    ota_qardorlar.append(dict_)

                elif acc.qarzdorlik > 0 and acc.qarzdorlik - acc.oquvchi_narxi < 0:
                    qarzdorlik_summasi += acc.qarzdorlik
                    seria = AccountSerializers(acc)
                    dict_ = dict(seria.data)
                    dict_['qarzi'] = acc.qarzdorlik
                    qarzdorlar.append(dict_)
            else:
                if acc.delete_qarzdorlik < 0 and acc.delete_qarzdorlik + acc.oquvchi_narxi > 0:
                    qarzdorlik_summasi += (acc.delete_qarzdorlik) * -1
                    seria = AccountSerializers(acc)
                    dict_ = dict(seria.data)
                    dict_['qarzi'] = acc.delete_qarzdorlik * -1
                    qarzdorlar.append(dict_)
                elif acc.delete_qarzdorlik < 0 and acc.delete_qarzdorlik + acc.oquvchi_narxi < 0:
                    qarzdorlik_summasi += (acc.delete_qarzdorlik) * -1
                    seria = AccountSerializers(acc)
                    dict_ = dict(seria.data)
                    dict_['qarzi'] = acc.delete_qarzdorlik * -1
                    ota_qardorlar.append(dict_)

        data['oquvchi_soni'] = account_number
        data['qarzdorlik_summasi'] = qarzdorlik_summasi
        data['delete_account'] = delete_account_number
        data['ota_qarzdorlar'] = ota_qardorlar
        data['qarzdorlar'] = qarzdorlar
        return Response(data=data)


class GeneralPaymentHistory(APIView):
    def get(self, request):
        list_ = []
        payments = Payment.objects.all()
        serializers = PaymentSerializers(payments, many=True)
        for i in serializers.data:
            account = Account.objects.get(id=i['account'])
            i['account'] = AccountSerializers(account).data
            list_.append(i)

        return Response(list_)


class CourseEditView(APIView):
    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        serializer = CourseSerializers(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = Course.objects.get(id=pk)
        serializer = CourseSerializers(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDeleteAccountView(APIView):
    def post(self, request, pk):
        serializer = PaymentSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class CourseViewSetForBot(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    permission_classes = [permissions.AllowAny]
