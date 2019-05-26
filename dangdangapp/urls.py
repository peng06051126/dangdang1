from django.urls import path
from dangdangapp import views


app_name = 'dangdangapp'
urlpatterns = [
    path('index/',views.index,name='index'),
    path('book_details/',views.book_details,name='book_details'),
    path('booklist/',views.booklist,name='booklist'),
    path('register/',views.register,name='register'),
    path('registerlogic/',views.registerlogic,name='registerlogic'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('checkname/',views.checkname,name='checkname'),
    path('checkpwd/',views.checkpwd,name='checkpwd'),
    path('registerok/',views.registerok,name='registerok'),
    path('delindex/',views.delindex,name='delindex'),
    # path('car/',views.car,name='car'),
    path('indent/',views.indent,name='indent'),
    path('add_book/',views.add_book,name='add_book'),
    path('delcar/',views.delcar,name='delcar'),
    path('del_book/',views.del_book,name='del_book'),
    path('compute/',views.compute,name='compute'),
    path('readd_book/',views.readd_book,name='readd_book'),
    path('ajax1/',views.ajax1,name='ajax1'),
    path('create_order/',views.create_order,name='create_order'),
    path('indentok/',views.indentok,name='indentok'),
    path('ajax2/',views.ajax2,name='ajax2'),
    path('ajax3/',views.ajax3,name='ajax3'),
    path('verify_emil/',views.verify_emil,name='verify_emil'),

]