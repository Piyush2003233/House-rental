from django.db import models

class UserRegistration(models.Model):
    full_name = models.CharField(max_length = 50)
    mobile_num = models.IntegerField()
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    is_approved=models.BooleanField(default=False)

    def __str__(self):
        return self.email_id

class ListingModel(models.Model):
    #details
    email_id = models.CharField(max_length=50,blank=True, null=True)
    view_count = models.IntegerField(default = 0)
    title = models.CharField(max_length=50)
    address = models.TextField(max_length=200)
    beds_qty = models.IntegerField(default=0)
    baths_qty = models.IntegerField(default=0)
    sqrft = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to = "images/")
    video=models.FileField(upload_to="video/",default='',null=True,blank=True)
    description = models.TextField(max_length=500)
    country = models.CharField("Area",max_length=50)
    apartment_type = models.CharField(max_length=50)
    #property
    property_id = models.IntegerField(default=0)
    rooms = models.IntegerField(default=0)
    #Amenities
    AC = models.BooleanField(default=False)
    builtin_wardrobe = models.BooleanField(default=False)
    dish_washer = models.BooleanField(default=False)
    floor_covering = models.BooleanField(default=False)
    medical = models.BooleanField(default=False)
    fencing = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    

    def __str__(self):
        return self.title


Product_Raings = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)

class ProperFeedback(models.Model):
    Property_name = models.ForeignKey("ListingModel", on_delete=models.CASCADE,blank=True, null=True)
    cust_data = models.ForeignKey("UserRegistration", on_delete=models.CASCADE,blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True)
    rating = models.CharField(max_length=20,choices=Product_Raings,default = '1')
    feedback = models.TextField()
    feed_pos = models.FloatField(default=0.0)
    feed_neg = models.FloatField(default=0.0)


class OwnerDetails(models.Model):
    Ownername=models.CharField(max_length=30)
    Owneremail=models.EmailField(unique=True)
    Ownerphone=models.PositiveIntegerField()
    Ownerstate=models.CharField(max_length=30)
    password=models.CharField(max_length=10)
    Amount=models.IntegerField(default=1)
    Approved=models.BooleanField(default=False)

    def __str__(self):
        return self.Owneremail


class Booking(models.Model):
    user_id=models.ForeignKey(UserRegistration,on_delete=models.CASCADE)
    owner_id=models.ForeignKey(OwnerDetails,on_delete=models.CASCADE,null=True)
    prop_id=models.ForeignKey(ListingModel,on_delete=models.CASCADE)
    document=models.FileField(upload_to='file/')
    boked=models.BooleanField(default=False)
    date=models.DateField(null=True)
    pyment=models.BooleanField(default=False)

class pymentdetails(models.Model):
    user=models.CharField(max_length=50)
    Owner=models.CharField(max_length=50)
    prop_name=models.CharField(max_length=50)
    PaymentVia=models.CharField(max_length=50)
    PaymentMethod=models.CharField(max_length=50)
    Amount=models.CharField(max_length=50)
    transactionId = models.TextField(default=None)
    orderDate = models.DateTimeField(auto_created=True,auto_now=True)
    