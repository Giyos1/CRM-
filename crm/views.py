from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CourseSerializers, AccountSerializers
from .models import Course, Account, Payment


class CourseList(ListAPIView):
    serializer_class = CourseSerializers
    queryset = Course.objects.all()


class CourseDetail(APIView):
    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        accounts = Account.objects.filter(course=course)
        serializers = AccountSerializers(accounts, many=True)
        payment = Payment.objects.filter()
        return Response(data=serializers.data)
