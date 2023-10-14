from django.contrib import admin
from account.models import User,Leave,expense,advanceExpense,Leads,Loads,KYCDetails
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
   

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name", "tc","is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name",'tc']}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name",'tc', "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)

class LeaveAdmin(admin.ModelAdmin):
    list_display=('leave_type','leave_from','leave_till','reason')
admin.site.register(Leave,LeaveAdmin)


class expenseAdmin(admin.ModelAdmin):
    list_display=('claim_category','claimed_amount','comments','photo')

admin.site.register(expense,expenseAdmin)    


class advanceExpenseAdmin(admin.ModelAdmin):
    list_display=('claim_category','claimed_amount','comments','photo')

admin.site.register(advanceExpense,advanceExpenseAdmin)    


class LeadsAdmin(admin.ModelAdmin):
    list_display=('truck_name','driver_name','phone','type','description','truck_no')

admin.site.register(Leads,LeadsAdmin) 



class LoadsAdmin(admin.ModelAdmin):
    list_display=('name','departure','arrival','weight','price','truck_type','material_type')

admin.site.register(Loads,LoadsAdmin) 


class KYCAdmin(admin.ModelAdmin):
    list_display=('truck_no','truck_driver_name','truck_type','phone_number','address','Aadhaar','PAN','RC')

admin.site.register(KYCDetails,KYCAdmin) 