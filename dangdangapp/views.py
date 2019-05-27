from datetime import datetime
import hashlib
import re
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from dangdangapp.models import TBooks, TSort, TAddress, TOrder, OrderItem, Confirm_string,TUser
import random,string
from dangdangapp.captcha.image import ImageCaptcha



def index(request):  #处理首页逻辑的视图函数
    username = request.COOKIES.get("username")
    a = TSort.objects.filter(parent_id=0)
    b = TSort.objects.filter(parent_id__gte=1)
    c = TBooks.objects.all().order_by('-shelf_time')[0:8]
    d = TBooks.objects.all()[0:9]
    e1 = TBooks.objects.all().order_by('-sales')
    f = e1.order_by('-shelf_time')[0:5]
    e = TBooks.objects.all().order_by('-sales')[0:10]
    return render(request,'dangdangapp/index.html',{'a':a,'b':b,'c':c,'d':d,'f':f,'e':e,'username':username})

def delindex(request):   #首页点击退出登录的视图函数
    red1 = redirect("dangdangapp:index")
    red1.delete_cookie("username")
    return red1

def book_details(request):  #图书详情页逻辑视图函数
    id = request.GET.get('id')
    g = TBooks.objects.filter(pk=id)[0]
    sort_id = g.sort_id
    h = TSort.objects.filter(id=sort_id)[0]
    parent_id = h.parent_id
    j = TSort.objects.filter(pk=parent_id)[0]
    username = request.COOKIES.get("username")
    return render(request,'dangdangapp/Book details.html',{'g':g,'h':h,'j':j,'username':username})

def booklist(request):   #图书列表页分类处理视图函数
    id1 = request.GET.get('id1')
    id2 = request.GET.get('id2')
    l = []
    number = request.GET.get('number')
    if not number:
        number=1
    if id2=='0':  #说明是一级分类
       two = TSort.objects.filter(parent_id=id1)  #查出所有的二级分类
       for i in two:
          l.append(i.id)
       w = TBooks.objects.filter(sort_id__in=l)
    else:
        w = TBooks.objects.filter(sort_id=id1)
    pagtor = Paginator(w, per_page=3)
    page = pagtor.page(number)
    return render(request,'dangdangapp/booklist.html',{'page':page,'number':number,'id1':id1,'id2':id2})


#================================注册模块============================================

def register(request):  #渲染注册页面
    return render(request,'dangdangapp/register.html')

def registerlogic(request):  #注册逻辑函数
    # try:
    #     with transaction.atomic():
            username = request.POST.get('txt_username')
            checkuser1 = request.POST.get('checkuser1')
            password = request.POST.get('txt_password')
            repassword = request.POST.get('txt_repassword')
            vcode = request.POST.get('txt_vcode')
            code = request.session.get('code')
            # flag = request.GET.get('flag')
            if vcode.upper()==code.upper() and password==repassword:
                passsword1 = make_password(password)
                new_user = TUser.objects.create(u_email=username,password=passsword1,u_name=checkuser1)
                u1 = TUser.objects.filter(u_email=username)[0]
                print(u1)
                res1 = redirect('dangdangapp:registerok')
                res1.set_cookie('username', username, max_age=60 * 60 * 24)
                request.session["regist"] = 'regist'
                    # code = make_confirm_string(new_user)
                send_email(username, username)
                if u1.has_confirm == True:
                    return res1

                return redirect('dangdangapp:delindex')

    # except:
    #     return render(request,'dangdangapp/register.html')

def registerok(request):
    return render(request,"dangdangapp/register ok.html")



#=========================邮箱验证=====================================
#邮箱验证部分
def hash_code(name, now):
    h = hashlib.md5()
    name += now
    h.update(name.encode())
    return h.hexdigest()

def make_confirm_string(new_user):
    print(new_user.u_email,new_user.id,102)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(new_user.u_email,now)
    print(new_user.id)
    Confirm_string.objects.create(code=code,user_id=new_user.id)
    return code

def send_email(username, code):
    subject, from_email, to = '来自的注册激活邮件', 'peng_l666@sina.com', '{}'.format(username)
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/dangdangapp/verify_emil/?code={}"target=blank>点击这里激活</a>，\欢迎你来验证你的邮箱，验证结束你就可以登录了！</p>'.format("127.0.0.1:8000",code)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def verify_emil(request):  #验证邮箱
    email = request.GET.get("code")
    if email:
        U = TUser.objects.filter(u_email=email)[0]
        U.has_confirm = True
        U.save()
        return redirect("dangdangapp:registerok")
    return HttpResponse("激活失败")

#==========================注册页ajax视图函数部分============================
#注册检验的ajax函数
def checkname(request):
    username = request.GET.get('username')
    z = re.findall('^1[0-9]{10}$|^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',username)
    if z:
        result = TUser.objects.filter(u_email=username)
        if result:
            return HttpResponse('1')
            # return HttpResponse('抱歉，该用户名已存在')

        else:
            return HttpResponse('2')
            # return HttpResponse('用户名合法')
    else:
        return HttpResponse('3')
        # return HttpResponse('用户名不符合规范')

def checkpwd(request):
    userpwd1 = request.GET.get('txt_password')
    userpwd2 = request.GET.get('txt_repassword')
    if userpwd1==userpwd2:
        return HttpResponse('验证通过')
    else:
        return HttpResponse('两次密码不一致请再次输入')

#生成验证码
def getcaptcha(request):
    image = ImageCaptcha()
    rand_code = random.sample(string.ascii_letters + string.digits, 1)
    rand_code = ''.join(rand_code)
    request.session['code'] = rand_code
    data = image.generate(rand_code)
    return HttpResponse(data,'image/png')

#=======================登录模块====================================
#登录模块
def login(request):
    return render(request,'dangdangapp/login.html')

def loginlogic(request):
    username = request.POST.get('txtUsername')
    userpwd = request.POST.get('txtPassword')
    u = TUser.objects.filter(u_email=username)[0]
    result1 = check_password(userpwd,u.password)
    result2 = TUser.objects.filter(u_email=username)
    code1 = request.POST.get('txtVerifyCode')
    code = request.session.get('code')
    if u.has_confirm == True:
        if result1 and code1.upper()==code.upper():
            res = redirect('dangdangapp:index')
            request.session['login'] = username
            res.set_cookie('username', result2[0].u_email, max_age=60 * 60 * 24)
            return res
    else:
        return HttpResponse("用户邮箱没激活请去激活")
    return render(request,'dangdangapp/login.html')

# def car(request):
#     return render(request,'dangdangapp/car.html')

#=============================订单页模块===================================
#订单页模块
def indent(request):
    flag_cart = request.GET.get('flag')
    # request.session['flag']= flag_cart
    username = request.session.get('login')
    print(username,199)
    cart = request.session.get('cart')
    if username:
        t = TUser.objects.get(u_email=username)
        addr = TAddress.objects.filter(user_id=t.id)
        print(addr,159)
        username = request.COOKIES.get("username")
        if username==None:
            flag_cart='flag_indent'
            request.session['flag_cart'] = flag_cart
            return render(request,'dangdangapp/login.html')
        return render(request,'dangdangapp/indent.html',{'addr':addr,'cart':cart,'username':username})
    else:
        return redirect('dangdangapp:login')

def create_order(request):
    cart = request.session.get('cart')
    username = request.session.get('login')
    y = TUser.objects.get(u_email=username)
    s = request.GET.get('ship_man1')
    d = request.GET.get('ship_man2')
    f = request.GET.get('ship_man3')
    g = request.GET.get('ship_man4')
    h = request.GET.get('ship_man5')
    c1 = request.GET.get('c1')
    print(c1)
    if c1:
        cc = TOrder.objects.create(tptal_price=cart.total_price, address_id=int(c1), user_id=y.id)
        for i in cart.cartitem:
            OrderItem.objects.create(book_id=i.book.id,order_id=cc.id, book_number=i.amount, subtotal=cart.total_price)

    else:
        hh = TAddress.objects.create(name=s,address=d,zipcode=f,telephone=g,phone=h,user_id=y.id)
        cc = TOrder.objects.create(tptal_price=cart.total_price, address_id=hh.id, user_id=y.id)
        for i in cart.cartitem:
            OrderItem.objects.create(book_id=i.book.id,order_id=cc.id,book_number=i.amount,subtotal=cart.total_price)

    return redirect('dangdangapp:indentok')

def indentok(request):
    username = request.COOKIES.get("username")
    del request.session['cart']
    if username == None:
        username = ''
    return render(request,'dangdangapp/indent ok.html',{'username':username})

#地址自动填充的ajax
def ajax1(request):
    a = request.GET.get('a')
    b = TAddress.objects.filter(address=a)
    # request.session[a] = a
    def mydefault(n):
        if isinstance(n,TAddress):
            return {'id':n.id,'name':n.name,'address':n.address,'zipcode':n.zipcode,'telephone':n.telephone,'phone':n.phone,"user_id":n.user_id}
    return JsonResponse(list(b),safe=False,json_dumps_params={"default":mydefault})


#===========================购物车模块=======================================
#购物车也逻辑部分
def add_book(request):
    id = request.GET.get('id')
    cart = request.session.get('cart')
    p = TBooks.objects.filter(pk=int(id))[0]
    # print(p)
    if cart is None:
        cart=Cart()
        cart.add_book_toCart(p)
        request.session['cart'] = cart
        return HttpResponse('1')
    # p = TBooks.objects.filter(pk=id)[0]
    else:
        cart.add_book_toCart(p)
        request.session['cart'] = cart
    return HttpResponse('2')

def readd_book(request):
    cart = request.session.get('cart')
    username = request.COOKIES.get("username")
    if username == None:
        username = ''
    return render(request, 'dangdangapp/car.html', {'cart': cart,'username':username})

def del_book(request):
    id = request.GET.get('id')
    cart = request.session.get('cart')
    cart.delete_book(int(id))
    request.session['cart'] = cart
    return redirect('dangdangapp:readd_book')

def delcar(request):
    red1 = redirect("dangdangapp:index")
    red1.delete_cookie("username")
    del request.session['login']
    return red1

#计算总价的视图函数
def compute(request):
    inp = request.GET.get('inp')
    id = request.GET.get('id')
    price = TBooks.objects.get(id=id).dd_price
    total_price = int(price) * int(inp)
    return HttpResponse(total_price)

#购物车页面加减数量变化价格的ajax
def ajax2(request):
    a = request.GET.get('id')
    b = TBooks.objects.filter(id=a)[0]
    cart=request.session.get('cart')
    cart.add_book_toCart(b)
    request.session['cart']=cart
    return HttpResponse(b.dd_price)

#购物车页面变化总价的ajax
def ajax3(request):
    id = request.GET.get('id')
    b = TBooks.objects.filter(id=id)[0]
    amount = request.GET.get('amount')
    cart = request.session.get('cart')
    cart.modify_cart(amount,id)
    request.session['cart'] = cart
    return HttpResponse(b.dd_price)





    # subject = '注册验证邮件'
    # text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    # html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.baidu.com</a>，\欢迎你来验证你的邮箱，验证结束你就可以登录了！</p>'.format('127.0.0.1',code)
    # msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [username])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

class Cartitem():
    def __init__(self,book,amount):
        self.amount = amount
        self.book = book

class Cart():
    def __init__(self):
        self.save_price = 0
        self.total_price = 0
        self.cartitem = []

    def sums(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.cartitem:
            self.total_price += i.book.dd_price * i.amount
            self.save_price += (i.book.price - i.book.dd_price) * i.amount


    def add_book_toCart(self,book):
        for i in self.cartitem:
            if i.book == book:
                i.amount += 1
                self.sums()
                return
        self.cartitem.append(Cartitem(book,1))
        self.sums()

    def modify_cart(self, amount,bookid):
        for i in self.cartitem:
            if i.book.id == bookid:
                i.amount = amount
        self.sums()

    def delete_book(self, bookid):
        for i in self.cartitem:
            if i.book.id == bookid:
                # 修改书的状态
                self.cartitem.remove(i)
        self.sums()