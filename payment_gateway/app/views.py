from django.shortcuts import render
from .models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings


def index(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        amount=int(request.POST['amount'])*100
        if name and email:
            client=razorpay.Client(auth=('add test code', 'add client code'))
            payment= client.order.create({'amount':amount, 'currency': 'INR','payment_capture':'1' })
            order=Details(name=name, email=email, amount=amount, payment_id=payment['id'])
            order.save()
            return render(request, 'index.html', {'payment':payment, 'name':name})
        return render(request, 'index.html',{'alert':'Please enter details '})
    return render (request, 'index.html')


def mail(from_mail,name,to_mail):
    subject='Registration ticket'
    from_email=from_mail
    name=name
    msg='<h1>Hii <b>{{name}}<b>, <br>You have successfully registered for new year ticket </h1>'
    to_email=to_mail
    send_mail(subject,msg,from_email,[to_email])
    sendmail=EmailMultiAlternatives(subject,msg,from_email,[to_email])
    sendmail.content_subtype='html'
    sendmail.send()



@csrf_exempt
def success(request):
    if request.method=="POST":
        a=request.POST
        order_id=""
        for key, item in a.items():
            if key=="razorpay_order_id":
                order_id=item
                break
        user=Details.objects.filter(payment_id=order_id).first()
        user.paid=True
        from_mail=settings.EMAIL_HOST_USER
        to_mail=user.email
        name=user.name
        user.save()
        mail(from_mail,to_mail,name)
        return render(request, 'success.html')
    return render(request, 'index.html')
