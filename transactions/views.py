from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
# Create your views here.

from rest_framework import authentication,permissions
from transactions.models import Calorie
from transactions.serializers import CalorieSerializer
from rest_framework.response import Response

class CalorieListCreateView(APIView):

    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes= [authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]



    def get(self,request):

        auth_user = request.user

        qs = Calorie.objects.filter(owner=auth_user)

        serializer_instance = CalorieSerializer(qs,many=True)

        return Response(serializer_instance.data)


    def post(self,request):

        form_data = request.data

        auth_user = request.user

        serializer_instance = CalorieSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save(owner=auth_user)

            return Response(serializer_instance.data)

        else:

            return Response(serializer_instance.errors)

from transactions.permissions import isowner

class CalorieRetrieveUpdateDeleteView(APIView):

    authentication_classes=[authentication.TokenAuthentication]
    #authentication_classes=[authentication.BasicAuthentication]

    #permission_classes= [permissions.IsAuthenticated]

    permission_classes=[isowner]

    def get(self,request,pk=None):

        #qs = Calorie.objects.get(id=pk)

        qs = get_object_or_404(Calorie,id=pk)

        self.check_object_permissions(request,qs)

         
        serializer_instance = CalorieSerializer(qs)

        return Response(serializer_instance.data)

    def put(self,request,pk=None):

        #instance = Calorie.objects.get(id=pk)
        instance =get_object_or_404(Calorie,id=pk)
        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = CalorieSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(serializer_instance.data)

        else:

            return Response(serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Calorie,id=pk)

        self.check_object_permissions(request,instance)

        instance.delete()

        return Response({"message":"deleted"})


from datetime import datetime  
from django.db.models import Sum
class calorieSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    #authentication_classes= [authentication.BasicAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
     
     auth_user_calorie = Calorie.objects.filter(owner=request.user)

     response_data={
         "todays_total":0,
         "monthly_total":0

     }

     cur_date = datetime.today().date()

     #today total

     todays_total= auth_user_calorie.filter(created_at=cur_date
                              ).aggregate(total=Sum("calorie")).get("total")

     response_data["todays_total"]=todays_total

     #monthly total

     cur_month = datetime.today().month

     cur_year = datetime.today().year

     auth_user_calorie.filter(created_at__month=cur_month,
                              created_at__year=cur_year).aggregate(total=Sum("calorie")).get("total")

     return Response(response_data)