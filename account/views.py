from logging import raiseExceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserRegisterationSerializer,UserLoginSerializer,LeaveViewSerializer,ExpenseSerializer,advanceExpenseSerializer,LeadsSerializer,LoadsSerializer,KYCSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.models import Leave,expense,advanceExpense,Leads,Loads,KYCDetails
from rest_framework.parsers import MultiPartParser, FormParser



#generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegisterationView(APIView):
        
  renderer_classes = [UserRenderer]

  def post(self,request,format=None):
            serializer = UserRegisterationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                  user = serializer.save()
                  user.set_password(request.data['password'])
                  user.save()
                  token = get_tokens_for_user(user)
                  
                  return Response({'msg':'Registeration Success','token':token},status=status.HTTP_201_CREATED)
                  
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
           
  


class UserLoginView(APIView):
      renderer_classes = [UserRenderer]
      def post(self,request,format=None):
             serializer = UserLoginSerializer(data = request.data)
             if serializer.is_valid(raise_exception=True):
                   email = serializer.data.get('email')
                   password = serializer.data.get('password')
                   user = authenticate(email = email,password=password)
                   if user is not None:
                         token=get_tokens_for_user(user)
      

                         return Response({'msg':'Login Success','token':token},status=status.HTTP_200_OK)
                   else:
                          return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}},status=status.HTTP_404_NOT_FOUND)
                   

             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
      
     



class LeaveDataView(APIView):
    authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        try:
            # The user is already authenticated via JWT token

            user = request.user
            
            # Extract the necessary leave data from the request data
            leave_type = request.data.get("leave_type")
            start_date = request.data.get("leave_from")
            end_date = request.data.get("leave_till")
            reason = request.data.get("reason")


            # Create a new LeaveData instance and save it in the database
            leave = Leave(forkey=user, leave_type=leave_type, leave_from=start_date, leave_till=end_date, reason = reason)
            leave.save()

            return Response({"message": "Leave stored successfully"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                   
      
    def get(self, request, format=None):
        try:
            # The user is already authenticated via JWT token
            user = request.user

            # Query the database to retrieve leave data for the authenticated user
            leave_data = Leave.objects.filter(forkey=user)

            # Serialize the leave data
            serializer = LeaveViewSerializer(leave_data, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class ExpenseCreateView(APIView):
    authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
       try:
            user = request.user
            claim_category = request.data.get("claim_category")
            claimed_amount = request.data.get("claimed_amount")
            comments = request.data.get("comments")
            photo = request.data.get("photo")

            expenseTable = expense(forkey=user,claim_category=claim_category, claimed_amount=claimed_amount, comments=comments, photo=photo)
            expenseTable.save()

            return Response({"message": "expense stored successfully"}, status=status.HTTP_201_CREATED)
       except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

    def get(self, request, format=None):
        try:
            user = request.user
            expense_data = expense.objects.filter(forkey=user)
            serializer = ExpenseSerializer(expense_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        



class advanceExpenseView(APIView):
    authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
       try:
            user = request.user
            claim_category = request.data.get("claim_category")
            claimed_amount = request.data.get("claimed_amount")
            comments = request.data.get("comments")
            photo = request.data.get("photo")

            expenseTable = advanceExpense(forkey=user,claim_category=claim_category, claimed_amount=claimed_amount, comments=comments, photo=photo)
            expenseTable.save()

            return Response({"message": "advance expense stored successfully"}, status=status.HTTP_201_CREATED)
       except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

    def get(self, request, format=None):
        try:
            user = request.user
            expense_data = advanceExpense.objects.filter(forkey=user)
            serializer = advanceExpenseSerializer(expense_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
            



class LeadsView(APIView):
      authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
      permission_classes = [IsAuthenticated]
    

      def post(self, request, format=None):
       try:
            user = request.user
            truck_name = request.data.get("truck_name")
            driver_name = request.data.get("driver_name")
            phone = request.data.get("phone")
            type = request.data.get("type")
            description = request.data.get("description")
            truck_no = request.data.get("truck_no")

            LeadsModel = Leads(forkey=user,truck_name=truck_name, driver_name=driver_name, phone=phone, type=type,description=description,truck_no=truck_no)
            LeadsModel.save()

            return Response({"message": "truck details stored successfully"}, status=status.HTTP_201_CREATED)
       except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

      def get(self, request, format=None):
        try:
            user = request.user
            leadsData = Leads.objects.filter(forkey=user)
            serializer = LeadsSerializer(leadsData, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 





class LoadsView(APIView):
      authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
      permission_classes = [IsAuthenticated]
    

      def post(self, request, format=None):
       try:
            user = request.user
            name = request.data.get("name")
            departure = request.data.get("departure")
            arrival = request.data.get("arrival")
            weight = request.data.get("weight")
            price = request.data.get("price")
            truck_type = request.data.get("truck_type")
            material_type = request.data.get("material_type")

            LoadsModel = Loads(forkey=user,name=name, departure=departure, arrival=arrival, weight=weight,price=price,truck_type=truck_type,material_type=material_type)
            LoadsModel.save()

            return Response({"message": "Loads details stored successfully"}, status=status.HTTP_201_CREATED)
       except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

      def get(self, request, format=None):
        try:
            user = request.user
            loadsData = Loads.objects.filter(forkey=user)
            serializer = LoadsSerializer(loadsData, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                    
              





class KYCView(APIView):
      authentication_classes = [JWTAuthentication]  # Add JWTAuthentication
      permission_classes = [IsAuthenticated]
    

      def post(self, request, format=None):
       try:
            user = request.user
            truck_no = request.data.get("truck_no")
            truck_driver_name = request.data.get("truck_driver_name")
            truck_type = request.data.get("truck_type")
            phone_number = request.data.get("phone_number")
            address = request.data.get("address")
            Aadhaar = request.data.get("Aadhaar")
            PAN = request.data.get("PAN")
            RC = request.data.get("RC")

            KYCModel = KYCDetails(forkey=user,truck_no=truck_no, truck_driver_name=truck_driver_name, truck_type=truck_type, phone_number=phone_number,address=address,Aadhaar=Aadhaar,PAN=PAN,RC=RC)
            KYCModel.save()

            return Response({"message": "KYC details stored successfully"}, status=status.HTTP_201_CREATED)
       except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       

      def get(self, request, format=None):
        try:
            user = request.user
            KYCData = KYCDetails.objects.filter(forkey=user)
            serializer = KYCSerializer(KYCData, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)                    
                            
        








      




      






      




             




                         
        


