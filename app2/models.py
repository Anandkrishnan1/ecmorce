from django.db import models

# Create your models here.
class reg_tb(models.Model):
	User_name=models.CharField(max_length=255)
	User_email=models.CharField(max_length=255)
	User_phno=models.CharField(max_length=255)
	User_pass=models.CharField(max_length=10)
	ENC_pass=models.TextField()




class cont_tb(models.Model):
	user_NAME=models.CharField(max_length=255)
	user_EMAIL=models.CharField(max_length=255)
	user_PHNO=models.CharField(max_length=10)
	user_MSG=models.CharField(max_length=255)

class pro_tb(models.Model):
	Pro_name=models.CharField(max_length=255)
	Pro_des=models.CharField(max_length=255)
	Pro_price=models.CharField(max_length=255)
	Pro_img=models.FileField(upload_to='product/')

class admin_reg(models.Model):
	Admin_name=models.CharField(max_length=255)
	Admin_email=models.CharField(max_length=255)
	Admin_phno=models.CharField(max_length=255)
	Admin_pass=models.CharField(max_length=255)
	Admin_img=models.FileField(upload_to='users/')




  
class cart_tb(models.Model):
	pid=models.ForeignKey(pro_tb, on_delete=models.CASCADE)
	uid=models.ForeignKey(reg_tb, on_delete=models.CASCADE)
	pro_qty=models.CharField(max_length=255)
	total_price=models.CharField(max_length=255)
	status=models.CharField(max_length=255,default="pending")






class pay_tb(models.Model):
	uid=models.ForeignKey(reg_tb, on_delete=models.CASCADE)
	total_amt=models.CharField(max_length=255)
	status=models.CharField(max_length=255,default="pending")
	state=models.CharField(max_length=255)
	zipcode=models.CharField(max_length=255)
