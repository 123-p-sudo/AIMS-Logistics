
from django.urls import path,include
from account.views import UserRegisterationView,UserLoginView,LeaveDataView,ExpenseCreateView,advanceExpenseView,LeadsView,LoadsView
from . import views
urlpatterns = [
    path('register/',UserRegisterationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    #path('profile/',UserProfileView.as_view(),name='profile'),
    path('leaveData/',LeaveDataView.as_view(),name='leaveData'),
    path('expenseUpload/', ExpenseCreateView.as_view(), name='upload_expense'),
    path('advanceExpenseUpload/', advanceExpenseView.as_view(), name='upload_advanceExpense'),
    path('LeadsUpload/', LeadsView.as_view(), name='upload_lead'),
    path('LoadsUpload/', LoadsView.as_view(), name='upload_load'),

]
