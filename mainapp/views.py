from django.shortcuts import render, redirect, HttpResponse
from .models import UserRegistration, ListingModel,OwnerDetails,Booking,ProperFeedback,pymentdetails
from .forms import UserForm, ListForm
from django.db.models import Q
from django.http import HttpResponse
from .filters import FilterDemo
from datetime import date
import itertools 
# text blob
from textblob import TextBlob
from django.db.models import Q
# Importing the NaiveBayesAnalyzer classifier from NLTK
from textblob.sentiments import NaiveBayesAnalyzer

def RegisterUSerView(request):
    form = UserForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration.html')

def LoginUserView(request):
    if request.POST:
        try:
            model = UserRegistration.objects.get(email_id=request.POST['email_id'])
            if model.password == request.POST['password']:
                request.session['User_email'] = model.email_id
                return redirect('UserIndexPage')
            else:
                return render(request,'login.html',{'error': "INCORRECT PASSWORD" })
        except:
            return render(request,'login.html',{'error': "INCORRECT USERNAME" })
    return render(request, 'login.html')



def Add_Listing(request):
    if 'User_email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['User_email'])
        if user_model.is_approved==True:
            if request.POST:
                form = ListForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    list_model = ListingModel.objects.latest('id')
                    list_model.email_id = user_model.email_id
                    list_model.save()
                    return redirect('myproperty')
        else:
            return render(request, 'add_list.html',{'approve':'Superuser Not Approved You'})
        return render(request, 'add_list.html',{'users_data':user_model})
    else:
        return redirect('login')

def Update_Owner_Property(request,id):
    if 'Owneremail' in request.session.keys():
        obj = ListingModel.objects.get(id=id)
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        if request.POST:
            obj.title = request.POST['title']
            obj.address = request.POST['address']
            obj.beds_qty = request.POST['beds_qty']
            obj.baths_qty =request.POST['baths_qty']
            obj.sqrft = request.POST['sqrft']
            obj.price = request.POST['price']
            img = request.FILES.get('image')
            video = request.FILES.get('video')
            if img != None:
                obj.image = img
            obj.description = request.POST['description']
            obj.country = request.POST['country']
            obj.apartment_type = request.POST['apartment_type']
            obj.rooms = request.POST['rooms']
            ac = request.POST.get('AC')
            if ac == "on":
                obj.AC = True
            else:
                obj.AC = False
            bw = request.POST.get('builtin_wardrobe')
            if bw == 'on':
                obj.builtin_wardrobe = True
            else:
                obj.builtin_wardrobe = False
            dw = request.POST.get('dish_washer')
            if dw == "on":
                obj.dish_washer = True
            else:
                obj.dish_washer = False
            fc = request.POST.get('floor_covering')
            if fc == "on":
                obj.floor_covering = True
            else:
                obj.floor_covering = False
            med = request.POST.get('medical')
            if med == "on":
                obj.medical = True
            else:
                obj.medical = False
            fen = request.POST.get('fencing')
            if fen == "on":
                obj.fencing = True
            else:
                obj.fencing = False
            inte = request.POST.get('internet')
            if inte == "on":
                obj.internet = True
            else:
                obj.internet = False
            obj.save()
            return redirect('OwnerProfileView',id)
        return render(request, 'owner_add_list.html',{'obj':obj,'owner_data':user_model})
    else:
        return redirect('ownerlogin')

def AllListView(request):
    if 'User_email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['User_email'])
        list_model = ListingModel.objects.all()  
        if request.GET:
            try:
                q = request.GET.get('search_data')
                print(q)
                print("Q Call")
            except:
                q = None
                print("No Q")
            
            if q != None and request.GET['search_data'] != None:
                apartmenttype = ListingModel.objects.all()
                apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                print("Q Collect")
                return render(request, 'listing.html', {'apartment1':apartment,'apartment':apartmenttype})
            else: 
                search = request.GET.get('text')
                pricefilter = request.GET.get('pricefilter')
                apartmenttype = ListingModel.objects.all()
                print("Q other Data")
                apartment = request.GET.get('apartment_type')
                if apartment != '':
                    list_model = ListingModel.objects.filter(apartment_type=apartment).order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)

                if pricefilter == 'low':
                    list_model = ListingModel.objects.all().order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                elif pricefilter == 'high':
                    list_model = ListingModel.objects.all().order_by('-price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                else:
                    list_model = ListingModel.objects.all()
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype,'users_data':user_model})
        else:
            print("Q POST")
            apartmenttype = ListingModel.objects.all()
            print("Q POst DAta")
            list_model = ListingModel.objects.all().filter(available=True)
            user_filter = FilterDemo(request.GET, queryset=list_model)
        list_model = ListingModel.objects.all()
        user_filter = FilterDemo(request.GET, queryset=list_model)
        return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype,'users_data':user_model})
        
    else:
        if request.GET:
            try:
                q = request.GET.get('search_data')
                print(q)
                print("Q Call")
            except:
                q = None
                print("No Q")
            
            if q != None and request.GET['search_data'] != None:
                apartmenttype = ListingModel.objects.all()
                apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                print("Q Collect")
                return render(request, 'listing.html', {'apartment1':apartment,'apartment':apartmenttype})
            else: 
                search = request.GET.get('text')
                pricefilter = request.GET.get('pricefilter')
                apartmenttype = ListingModel.objects.all()
                print("Q other Data")
                apartment = request.GET.get('apartment_type')
                if apartment != '':
                    list_model = ListingModel.objects.filter(apartment_type=apartment).order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)

                if pricefilter == 'low':
                    list_model = ListingModel.objects.all().order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                elif pricefilter == 'high':
                    list_model = ListingModel.objects.all().order_by('-price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                else:
                    list_model = ListingModel.objects.all()
                    user_filter = FilterDemo(request.GET, queryset=list_model)

        else:
            print("Q POST")
            apartmenttype = ListingModel.objects.all()
            print("Q POst DAta")
            list_model = ListingModel.objects.all()
            user_filter = FilterDemo(request.GET, queryset=list_model)
    return render(request, 'listing.html', {'all_list': user_filter,'apartment':apartmenttype})



def OwnerAllListView(request):
    if 'Owneremail' in request.session.keys():
        user=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        list_model = ListingModel.objects.all().filter(available=True)  
        if request.GET:
            try:
                q = request.GET.get('search_data')
                print(q)
                print("Q Call")
            except:
                q = None
                print("No Q")
            
            if q != None and request.GET['search_data'] != None:
                apartmenttype = ListingModel.objects.all()
                apartment = ListingModel.objects.filter(Q(title__icontains=q) | Q(address__icontains=q) | Q(description__icontains=q))
                print("Q Collect")
                return render(request, 'Ownerlisting.html', {'apartment1':apartment,'apartment':apartmenttype,'owner_data':user})
            else: 
                search = request.GET.get('text')
                pricefilter = request.GET.get('pricefilter')
                apartmenttype = ListingModel.objects.all()
                print("Q other Data")
                apartment = request.GET.get('apartment_type')
                if apartment != '':
                    list_model = ListingModel.objects.filter(apartment_type=apartment).order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)

                if pricefilter == 'low':
                    list_model = ListingModel.objects.all().order_by('price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                elif pricefilter == 'high':
                    list_model = ListingModel.objects.all().order_by('-price')
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                else:
                    list_model = ListingModel.objects.all().filter(verified=True)
                    user_filter = FilterDemo(request.GET, queryset=list_model)
                return render(request, 'Ownerlisting.html', {'all_list': user_filter,'apartment':apartmenttype,'owner_data':user})
        else:
            print("Q POST")
            apartmenttype = ListingModel.objects.all()
            print("Q POst DAta")
            list_model = ListingModel.objects.all().filter(available=True)
            user_filter = FilterDemo(request.GET, queryset=list_model)
        list_model = ListingModel.objects.all()
        user_filter = FilterDemo(request.GET, queryset=list_model)
        return render(request, 'Ownerlisting.html', {'all_list': user_filter,'apartment':apartmenttype,'owner_data':user})
        
    else:
        return redirect('ownerlogin')

def UserIndexPage(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        # list_model = ListingModel.objects.all().order_by('-id')[:3]
        
        prod = ListingModel.objects.all()
        
        data_set = {}
        for i in prod:
            sub_dict = {}
            print("------------------")
            print(i.id)
            fda = ProperFeedback.objects.filter(Property_name=i)
            tot_pos = 0.0
            tot_ret = 0.0
            count = 0
            for j in fda:
                count += 1
                # print("-+++-")
                # print(j.cust_name)
                # print(j.feed_pos)
                tot_pos += float(j.feed_pos)
                tot_ret += float(j.rating)
                # print(j.rating)
                # print("-+++-")
            
            if tot_pos > 0:
                tot_pos = float(tot_pos/count)
            else:
                tot_pos = 0.1
            if tot_ret > 0:
                tot_ret = float(tot_ret/count)
            else:
                tot_ret = 1
            sub_dict['count'] = count
            sub_dict['pos'] = f"{tot_pos:.4f}"
            sub_dict['ret'] = f"{tot_ret:.2f}"
            
            data_set[i] = sub_dict
            # print(sub_dict)
            print(f"total user = {count}")
            print(f"total positive = {tot_pos:.4f}")
            print(f"total rating = {tot_ret:.2f}")
            print("------------------")
        print(data_set)
        
  
        # printing original dict
        print("The original dictionary : " + str(data_set))
        
        # using sorted()
        # Sort nested dictionary by key
        res = sorted(data_set.items(), key = lambda x: x[1]['pos'])
        data_set = dict(reversed(res))
        # print result
        print("The sorted dictionary by marks is : " + str(res))
        print("The reversed dictionary by marks is : " + str(data_set))
        N = 6 
        data_set = dict(itertools.islice(data_set.items(), N))
        # return render(request,'deshbord.html',{'data_set':data_set})
        
        # return render(request, 'index.html',{'top':list_model,'users_data':user,'data_set':data_set})
        return render(request, 'index.html',{'users_data':user,'data_set':data_set})
    else:
        list_model = ListingModel.objects.all().order_by('-id')[:3]
        return render(request, 'index.html',{'top':list_model})
        

def OwnerIndexView(request):
    if 'Owneremail' in request.session.keys():
        user=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        list_model = ListingModel.objects.all().order_by('-id')[:3]
        return render(request, 'Ownerindex.html',{'top':list_model,'owner_data':user})
    else:
        return redirect('ownerlogin')
    

def ProfileView(request, id):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        model = ListingModel.objects.get(id=id)
        q = str(model.country)
        model.view_count += 1
        model.save()
        dataset = ''
        try:
            dataset = ListingModel.objects.filter(Q(country__icontains=q)| Q(address__icontains=q))[0:4]
        except:
            dataset = ListingModel.objects.all()[0:4]
        feeds = ProperFeedback.objects.filter(Property_name=model)
        try:
            User_feed = ProperFeedback.objects.get(Property_name=model,cust_data=user)
            if request.POST:
                User_feed.Property_name = model
                User_feed.cust_name = user
                User_feed.rating = request.POST['rating']
                User_feed.feedback = request.POST['feedback']
                
                test = str(request.POST['feedback'])
                # Applying the NaiveBayesAnalyzer
                blob_object = TextBlob(test, analyzer=NaiveBayesAnalyzer())
                # Running sentiment analysis
                analysis = blob_object.sentiment
                print(analysis)
                pos = float("{:.2f}".format(analysis.p_pos))
                neg = float("{:.2f}".format(analysis.p_neg))
                
                obj.feed_pos=pos
                obj.feed_neg=neg
                User_feed.save()
            return render(request, 'property-single.html', {'data_set':dataset,'data': model,'users_data':user,'feed_data':feeds,'feed':User_feed})
        except:
            if request.POST:
                obj = ProperFeedback()
                obj.Property_name = model
                obj.cust_data = user
                obj.rating = request.POST['rating']
                obj.feedback = request.POST['feedback']
                
                test = str(request.POST['feedback'])
                # Applying the NaiveBayesAnalyzer
                blob_object = TextBlob(test, analyzer=NaiveBayesAnalyzer())
                # Running sentiment analysis
                analysis = blob_object.sentiment
                print(analysis)
                pos = float("{:.5f}".format(analysis.p_pos))
                neg = float("{:.5f}".format(analysis.p_neg))

                obj.feed_pos=pos
                obj.feed_neg=neg

                
                
                obj.save()
            
        return render(request, 'property-single.html', {'data_set':dataset,'data': model,'users_data':user,'feed_data':feeds})
    else:
        return redirect('login')

def OwnerProfileView(request, id):
    if 'Owneremail' in request.session.keys():
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        model = ListingModel.objects.get(id=id)
        model.view_count += 1
        model.save()
        return render(request, 'ownerproperty-single.html', {'data': model,'owner_data':user_model})
    else:
        return redirect('ownerlogin')

def Owner_myproperty(request):
    if 'Owneremail' in request.session.keys():
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        all_list = ListingModel.objects.filter(email_id=request.session['Owneremail'])
        return render(request, 'ownermyproperty.html', {'all_list': all_list,'owner_data':user_model})
    else:
        return redirect('login')

def MyPropertyView(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        all_list = ListingModel.objects.filter(email_id=request.session['User_email'])
        return render(request, 'myproperty.html', {'all_list': all_list,'users_data':user})
    else:
        return redirect('login')


def deleteproperty(request, id):
    model = ListingModel.objects.get(id=id)
    model.delete()
    return redirect('myproperty')


def logout(request):
    if 'User_email' in request.session.keys():
        del request.session['User_email']
        return redirect('UserIndexPage')
    else:
        return redirect('UserIndexPage')

def ownersignup(request):
    if request.POST:
        model= OwnerDetails()
        model.Ownername=request.POST['Ownername']
        model.Owneremail=request.POST['Owneremail']
        model.Ownerphone=request.POST['Ownerphone']
        model.Ownerstate=request.POST['Ownerstate']
        model.password=request.POST['password']
        model.save()
        request.session['Owneremail']=model.Owneremail
        print(request.session['Owneremail'])
        return redirect('ownerlogin')
    return render(request,'ownersignup.html')

def ownerlogin(request):
    if request.POST:
        Owneremail=request.POST['Owneremail']
        password=request.POST['password']
        try:
            mo=OwnerDetails.objects.get(Owneremail=Owneremail)
            if mo.password==password:
                request.session['Owneremail']=mo.Owneremail
                return redirect('alldata')
            else:
                return render(request,'ownerlogin.html',{'error': "INCORRECT PASSWORD" })
        except:
            return render(request,'ownerlogin.html',{'error': "INCORRECT USERNAME" })
    return render(request,'ownerlogin.html')

def owner_Add_Listing(request):
    if 'Owneremail' in request.session.keys():
        user_model = OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        print(user_model)
        model=ListingModel()
        count=0
        if request.POST:
            form = ListForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                list_model = ListingModel.objects.latest('id')
                list_model.email_id = user_model.Owneremail
                list_model.property_id+=1
                list_model.save()        
                return redirect('Owner_myproperty')
        return render(request, 'owner_add_list.html',{'owner_data':user_model})
    else:
        return redirect('ownerlogin')

def prop_booking(request,id):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        prod=ListingModel.objects.get(id=id)
        if user.email_id == prod.email_id:
            return HttpResponse("<h2>You Are Owner Of This Property</h2>")
        else:
            owner=OwnerDetails.objects.get(Owneremail=prod.email_id)
            if request.POST and request.FILES:
                model=Booking()
                model.user_id=user
                model.owner_id=owner
                model.prop_id=prod
                model.document=request.POST and request.FILES['document']
                model.date=date.today()
                model.save()
                prod.available=False
                prod.rooms -= 1
                prod.save()
                return redirect ('UserBooks')
            return render(request,'booking.html',{'users_data':user,'prod':prod,'wait':'WAIT for approval'})
    else:
        return redirect('login')


def UserBooks(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        prod = Booking.objects.filter(user_id=user)
        
        return render(request,'UserBooks.html',{'users_data':user,'prod':prod})
    else:
        return redirect('login')

def viewBooks(request,id):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        prod = Booking.objects.get(id=id)
        return render(request,'UserspecBooks.html',{'users_data':user,'prod':prod})
    else:
        return redirect('login')




def alldata(request):
    if 'Owneremail' in request.session.keys():
        owner=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        book=Booking.objects.all().filter(owner_id=owner)
    return render(request,'alldata.html',{'book':book,'owner_data':owner})


def edit(request,id):
    if 'Owneremail' in request.session.keys():
        owner=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        book=Booking.objects.get(id=id)
        return render(request,'editbook.html',{'book':book,'owner_data':owner})
    else:
        return redirect('ownerlogin')

def update(request,id):
    if 'Owneremail' in request.session.keys():
        book=Booking.objects.get(id=id)
        if request.POST:
            book.boked=request.POST['boked']
            book.date=date.today()
            book.save()

            return redirect('alldata')
        else:
            pass
    return render(request,'editbook.html')

def userbuy(request):
    if 'Owneremail' in request.session.keys():
        owner=OwnerDetails.objects.get(Owneremail=request.session['Owneremail'])
        mod=Booking.objects.filter(owner_id=owner)
        return render(request,'userbuy.html',{'owner':owner,'mod':mod})
    else:
        return redirect('ownerlogin')

def Owner_logout(request):
    if 'Owneremail' in request.session.keys():
        del request.session['Owneremail']
        return redirect('ownerlogin')
    else:
        return redirect('ownerlogin')

def getdetails(request,id):
    if 'User_email' in request.session.keys():
        user_model = UserRegistration.objects.get(email_id=request.session['User_email'])
        prod=Booking.objects.get(id=id)
        print(prod.id)
        return render(request,'getdetails.html',{'prod':prod})
    else:
        return redirect('login')
        
def main(request):
    return render(request,'login/index.html')





import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def paymentofbooking(request):       
        if request.method=="POST":        
            request.session['user'] = request.POST['user']
            request.session['owner'] = request.POST['owner']
            request.session['id'] = request.POST['id']
            request.session['prop_name'] = request.POST['prop_name']
            request.session['price'] = request.POST['price']
            request.session['PaymentVia'] = "Online"
            request.session['PaymentMethod'] = "Razorpay"
            request.session['TransactionId'] = ""
            print(request.session['user'],request.session['owner'],request.session['price'],type(request.session['price']),)
            return redirect('razorpayView')                   

RAZOR_KEY_ID = 'rzp_test_8iwTTjUECLclBG'
RAZOR_KEY_SECRET = '0q8iXqBL1vonQGVQn4hK1tYg'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['price'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['price'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)

            #Order Save Code
            orderModel = pymentdetails()
            orderModel.user = request.session['user']
            orderModel.Owner = request.session['owner']
            orderModel.prop_name = request.session['prop_name']
            orderModel.PaymentVia = request.session['PaymentVia']
            orderModel.PaymentMethod = request.session['PaymentMethod']
            orderModel.Amount = request.session['price']
            orderModel.transactionId = payment_id
            orderModel.save()
            d=Booking.objects.get(id=request.session['id'])
            d.pyment=True
            d.save()
            del request.session['id']
            # render success page on successful caputre of payment
            return redirect('orderSuccessView')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello1")
       # if other than POST request is made.
        return HttpResponseBadRequest()

def orderSuccessView(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        
        return render(request,'complete.html',{'users_data':user})
    else:
        return redirect('login')
def ordertable(request):
    if 'User_email' in request.session.keys():
        user=UserRegistration.objects.get(email_id=request.session['User_email'])
        order=pymentdetails.objects.filter(user=user.full_name)
        return render(request,'ordertable.html',{'users_data':user,'order':order})
    else:
        return redirect('login')