from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
import os
import random
import string
from django.conf import settings
from django.core.mail import send_mail
import hashlib
# Create your views here.
def index(request):
	return render(request,'index.html')

def about(request):
	return render(request,'about.html')

def coming(request):
	return render(request,'coming.html')		

def contact(request):
	if request.method=='POST':
		cnt_name=request.POST['cont_name']
		cnt_email=request.POST['cont_email']
		cnt_phno=request.POST['cont_phno']
		cnt_msg=request.POST['cont_msg']
		check=cont_tb.objects.filter(user_EMAIL=cnt_email)
		if check:
			return render(request,'contact.html',{"erroe":"Allready submitted"})
		else:
			add=cont_tb(user_NAME=cnt_name,user_EMAIL=cnt_email,user_PHNO=cnt_phno,user_MSG=cnt_msg)
			add.save()
			return render(request,"contact.html",{"success":"submitted successfully"})
	else:
		return render(request,'contact.html')

def login(request):
	if request.method=='POST':
		user_email=request.POST['reg_email']
		user_pass=request.POST['reg_pass']
		hashpass=hashlib.md5(user_pass.encode('utf8')).hexdigest()

		check=reg_tb.objects.filter(User_email=user_email,User_pass=user_pass,ENC_pass=hashpass)
		if check:
			for x in check:
				request.session['myid']=x.id
				request.session['myname']=x.User_name
			return HttpResponseRedirect('/')
		else:
		     return render(request,'login.html',{"error":"incorrect details"})
	else:
		return render(request,'login.html')	 



def logout(request):
	if request.session.has_key('myid'):
		del request.session['myid']
		
	return HttpResponseRedirect("/")




	
def register(request):
	if request.method=='POST':
	  user_name=request.POST['reg_name']
	  user_email=request.POST['reg_email']
	  user_phno=request.POST['reg_phno']
	  user_pass=request.POST['reg_pass']
	  hashpass=hashlib.md5(user_pass.encode('utf8')).hexdigest()
	  check=reg_tb.objects.filter(User_email=user_email)
	  if check:
	  	return render(request,"register.html",{"error":"Allready registered "})
	  else:
	  	add=reg_tb(User_name=user_name,User_email=user_email,User_phno=user_phno,User_pass=user_pass,ENC_pass=hashpass)
	  	add.save()
	  	x = ''.join(random.choices(user_name + string.digits, k=8))
	  	y = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
	  	subject = 'welcome to ecomerce'
	  	message = f'Hi {user_name}, thank you for registering in ecommerece . your user username: {user_email} and  password: {user_pass}.'
	  	email_from = settings.EMAIL_HOST_USER 
	  	recipient_list = [user_email, ] 
	  	send_mail( subject, message, email_from, recipient_list ) 
	  	return render(request,'login.html',{'msg':"succesfuly saved"})
	else:
		return render(request,'register.html')

		



def shop(request):
	data=pro_tb.objects.all()
	return render(request,'shop.html',{"prd":data})

def single(request):
	if  request.session.has_key("myid"): 
		pid=request.GET['uid']
		prod=pro_tb.objects.filter(id=pid)
		# print("pid","00000000000000000000")
		return render(request,'single.html',{"prde":prod})	

	else:
		return HttpResponseRedirect('/login/')					

def add_tocart(request):
	if request.session.has_key("myid"):
		if request.method=='POST':
			pid=request.GET['uid']
			data=pro_tb.objects.filter(id=pid)
			for x in data:
				unitprice=int(x.Pro_price)
			pidd=pro_tb.objects.get(id=pid)
			uid=request.session['myid']
			uidd=reg_tb.objects.get(id=uid)
			qty=request.POST['qty']	
			total_price=(int(qty)*unitprice)
			delv=total_price+((unitprice*10)/100)
			check=cart_tb.objects.filter(pid=pidd,uid=uidd,status="pending")
			prod=cart_tb.objects.filter(uid=uid,status="pending")
			if check:
				for x in check:
				# cartid=x.id
				# print(cartid,"+++++++++++++++")
				# cart_tb.objects.filter(id=cartid).update(total_price=delv,pro_qty=qty)
					prd=x.pid
					if pidd==prd:
						cart_tb.objects.filter(pid=pidd,status="pending").update(total_price=delv,pro_qty=qty)
						return render(request,"cart.html",{"error":"already in cart","data":prod})
					else:
						return render(request,"cart.html")
                	
			else:
				add=cart_tb(pid=pidd,uid=uidd,pro_qty=qty,total_price=delv)
				add.save()
				return HttpResponseRedirect('/cart/')					

		else:
			pid=request.GET['uid']
			prod=pro_tb.objects.filter(id=pid)
			# print("pid","00000000000000000000")
			return render(request,'single.html',{"prde":prod})	
			
	else:
		return HttpResponseRedirect('/login/')				


def additem(request):
	prdid=request.GET['cid']
	qty=request.POST['quantity']
	# if qty == '0':
	# 	abcd=cart_tb.objects.filter(id=prdid).delete()
	# 	return HttpResponseRedirect('/cart/')
	# else:
		# crtid=request.GET['uid']
	data=cart_tb.objects.filter(id=prdid)
	for x in data:
		unitprice=int(x.pid.Pro_price)
	total_price=(int(qty)*unitprice)
	delv=total_price+((unitprice*10)/100)
	abcd=cart_tb.objects.filter(id=prdid).update(pro_qty=qty,total_price=delv)
	return HttpResponseRedirect('/cart/')		




def cart(request):
	if request.session.has_key('myid'):
		uid=request.session['myid']
		prod=cart_tb.objects.filter(uid=uid,status="pending")
		count=cart_tb.objects.filter(uid=uid,status="pending").count()
		total=0
		if prod:
			for x in prod:
				price=x.total_price
				
				total=total+float(price)
			

				



			return render(request,"cart.html",{"data":prod,"count":count,"total":total})
		else:
			return HttpResponseRedirect('/shop/')

	else:
		return HttpResponseRedirect('/login/')
		
def delete(request):
	prdid=request.GET['cid']
	abcd=cart_tb.objects.filter(id=prdid).delete()
	return HttpResponseRedirect('/cart/')





def payment(request):
	if request.session.has_key('myid'):
		if request.method=='POST':
			uid=request.session['myid']
			uidd=reg_tb.objects.get(id=uid)
			amount=request.POST['amount']
			# data=pay_tb.objects.filter(uid=uidd,amount=Amount,status='pending')
			# if data:
			add=pay_tb(uid=uidd,total_amt=amount,status='paid')
			# save= int(123)
			add.save()
			cart=cart_tb.objects.filter(uid=uidd,status='pending').update(status='odered')
			# print(save,"***********************")
			return HttpResponseRedirect("/")
		else:
			amount=request.GET['Amount']
			return render(request,"payment.html",{"amount":amount})





##################################################################################################################################################################################################################################################

             # admin page #


##################################################################################################################################################################################################################################################
					
def blank(request):
	return render(request,"admin/blank.html")


def buttons(request):
	return render(request,"admin/buttons.html")


def charts(request):
	return render(request,"admin/charts.html")


def grids(request):
	return render(request,"admin/grids.html")


def icons(request):
	return render(request,"admin/icons.html")				


def inbox_details(request):
	productview=pro_tb.objects.all()
	return render(request,"admin/inbox_details.html",{'users':productview})	

def proupdate(request):
	if request.method == "POST":
		pro_name=request.POST['productname']
		pro_des=request.POST['details']
		pro_price=request.POST['price']
		check=request.POST['check']
		pid=request.GET['uid']

		if check =="yes":
			pro_img=request.FILES['Images']
			old_img=pro_tb.objects.filter(id=pid)
			new_img=pro_tb.objects.get(id=pid)
			for x in old_img:
				image=x.Pro_img.url
				pathtoimage=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+image
				if os.path.exists(pathtoimage):
					os.remove(pathtoimage)
					print('Successfully deleted')
			new_img.Pro_img=pro_img
			new_img.save()
		pro_tb.objects.filter(id=pid).update(Pro_name=pro_name,Pro_des=pro_des,Pro_price=pro_price)
		return HttpResponseRedirect('/inboxdetails/')
			
	else:
		pid=request.GET['uid']
		product=pro_tb.objects.filter(id=pid)
		return render(request,"admin/pro_update.html",{'usres':product})




def inbox(request):
	if request.method=='POST':
		pro_img=request.FILES['proimg']
		pro_name=request.POST['productname']
		pro_des=request.POST['details']
		pro_price=request.POST['price']
		
		check=pro_tb.objects.filter(Pro_name=pro_name,Pro_des=pro_des,Pro_price=pro_price)
		if check:
			return render(request,"admin/inbox.html")
		else:
			add=pro_tb(Pro_name=pro_name,Pro_des=pro_des,Pro_price=pro_price,Pro_img=pro_img)
			add.save()
			return render(request,"admin/inbox.html")
	else:
		return render(request,"admin/inbox.html")
			


	return render(request,"admin/inbox.html")	


def adim_signup(request):
	if request.method=='POST':
	  admin_name=request.POST["name"]
	  admin_email=request.POST["email"]
	  admin_phno=request.POST["phno"]
	  admin_pass=request.POST["password"]
	  admin_img=request.FILES["img"]
	  check=admin_reg.objects.filter(Admin_email=admin_email)
	  if check:
	  	return render(request,"admin/signup.html",{"error":"Allready registered "})
	  else:
	  	add=admin_reg(Admin_name=admin_name,Admin_email=admin_email,Admin_phno=admin_phno,Admin_pass=admin_pass,Admin_img=admin_img)
	  	add.save()
	  	x = ''.join(random.choices(admin_name + string.digits, k=8))
	  	y = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
	  	subject = 'welcome to ecomerce'
	  	message = f'Hi {admin_name}, thank you for registering in ecommerece . your user username: {admin_email} and  password: {admin_pass}.'
	  	email_from = settings.EMAIL_HOST_USER 
	  	recipient_list = [admin_email, ] 
	  	send_mail( subject, message, email_from, recipient_list ) 
	  	return render(request,'admin/login.html',{'msg':"succesfuly saved"})
	else:
		return render(request,'admin/signup.html')





def login_admin(request):
	if request.method=='POST':
		admin_email=request.POST['email']
		admin_pass=request.POST['password']
		check=admin_reg.objects.filter(Admin_email=admin_email,Admin_pass=admin_pass)
		if check:
			for x in check:
				request.session['newid']=x.id
				request.session['myname']=x.Admin_name
				request.session['myphoto']=x.Admin_img.url
			return HttpResponseRedirect('/indexadmin/')
		else:
		     return render(request,'admin/login.html',{"error":"incorrect details"})
	else:
		return render(request,'admin/login.html')	 
	

def logout_admin(request):
	if request.session.has_key('newid'):
		del request.session['newid']
		del request.session['myname']
		del request.session['myphoto']
		
	return HttpResponseRedirect('/loginadmin/')


def index_admin(request):
	return render(request,"admin/index.html")


def maps(request):
	return render(request,"admin/maps.html")	


def portlet(request):
	return render(request,"admin/portlet.html")


def price(request):
	return render(request,"admin/price.html")


def product(request):
	return render(request,"admin/product.html")


def singup(request):
	return render(request,"admin/singup.html")


def typography(request):
	return render(request,"admin/typography.html")





def passwordforget(request):
	if request.method=='POST':
		admin_email=request.POST["email"]
		admin_phno=request.POST["phno"]
		check=admin_reg.objects.filter(Admin_email=admin_email,Admin_phno=admin_phno)
		if check:
			# for x in check:
			# 	name=x.Admin_name
			# 	uid=x.id
			# 	passw=x.Admin_pass
			# x = ''.join(random.choices(name + string.digits, k=8))
			# y = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
			# subject = 'welcome to ecomerce'
			# message = f' current pass is{passw} link to passwordforget is http://127.0.0.1:8000/forgetpass/?uid={uid}.'
			# email_from = settings.EMAIL_HOST_USER 
			# recipient_list = [admin_email, ] 
			# send_mail( subject, message, email_from, recipient_list ) 
			return render(request,'admin/reset.html',{'data':check})
		else:
			return render(request,"admin/forget.html",{"error":"incorrect details"})
	else:
		return render(request,"admin/forget.html")
			
def restpass(request):
	if request.method == "POST":
		pid=request.GET['resid']
		newpass=request.POST['newpass']
		cnfpass=request.POST['confpass']
		if newpass == cnfpass:
			admin_reg.objects.filter(id=pid).update(Admin_pass=newpass)
			return HttpResponseRedirect('/loginadmin/')
	else: 
		return render (request ,"admin/reset.html",{"error":"passsword mismatch"})
    


	# return render(request,"admin/login.html")

def ajaxview(request):
	print("hello")
	pid=request.GET.get('proname')
	pro=pro_tb.objects.filter(id=pid)
	for x in pro:
		v=x.Pro_name
		w=x.Pro_des
		y=x.Pro_price
		z=x.Pro_img.url
	dat={"aa":v,"bb":w,"cc":y,"dd":z}
	print(dat)
	return JsonResponse(dat)