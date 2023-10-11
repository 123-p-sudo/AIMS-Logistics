
import attrs
from rest_framework import serializers
from account.models import User,Leave,expense,advanceExpense,Leads,Loads
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode


class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields=['id','name','email','password','password2','tc']
        extra_kwargs = {
            'password':{'write_only':True}
        }

      #validate password and confirm password 
    def  validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm password does not match')
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']    

class  UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']  



class LeaveViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields=['id','leave_type','leave_from','leave_till','reason']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = expense
        fields = ('claim_category', 'claimed_amount', 'comments','photo')        

        


class advanceExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model= advanceExpense
        fields = ('claim_category','claimed_amount','comments','photo')



class LeadsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Leads
        fields = ('truck_name','driver_name','phone','type','description','truck_no')



class LoadsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Loads
        fields = ('name','departure','arrival','weight','price','truck_type','material_type')        
