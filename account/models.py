from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser
)



# Create your models here.

#custom user models
class UserManager(BaseUserManager):
    def create_user(self, email, name,tc, password=None,password2=None):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,tc, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    id=models.BigAutoField(primary_key=True)
    name  = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name",'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
class Leave(models.Model):
    leave_type=models.CharField(max_length=50)
    leave_from=models.DateField()
    leave_till =models.DateField()
    reason = models.TextField() 
    forkey=models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.leave_type
     


class expense(models.Model):
    claim_category=models.CharField(max_length=50)
    claimed_amount=models.IntegerField()
    comments=models.TextField()
    photo = models.ImageField(upload_to="photo/%Y/%m/%d",blank=True) 
    forkey = models.ForeignKey(User, on_delete=models.CASCADE,default=1)  

    def __str__(self):
        return self.claim_category  
    



class advanceExpense(models.Model):
    claim_category=models.CharField(max_length=50)
    claimed_amount=models.IntegerField()
    comments=models.TextField()
    photo = models.ImageField(upload_to="photo/%Y/%m/%d",blank=True) 
    forkey = models.ForeignKey(User, on_delete=models.CASCADE,default=1)  

    def __str__(self):
        return self.claim_category    
    


class Leads(models.Model):
    truck_name=models.CharField(max_length=50)
    driver_name=models.CharField(max_length=25)
    phone=models.IntegerField()
    type = models.CharField(max_length=50)
    description=models.TextField()
    truck_no = models.IntegerField()
    forkey = models.ForeignKey(User, on_delete=models.CASCADE,default=1) 

    def __str__(self):
        return self.truck_name    


class Loads(models.Model):
    name=models.CharField(max_length=50)
    departure = models.CharField(max_length=25)
    arrival = models.CharField(max_length=50)
    weight =models.IntegerField()
    price =models.IntegerField()
    truck_type = models.CharField(max_length=100)
    material_type = models.CharField(max_length=100)
    forkey = models.ForeignKey(User, on_delete=models.CASCADE,default=1) 
    

    def __str__(self):
        return self.name      