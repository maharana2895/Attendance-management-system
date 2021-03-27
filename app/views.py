from django.shortcuts import render, HttpResponse, redirect
from .forms import loginForm
from django.contrib.auth import authenticate, login
from .api import check_cookie, check_login, get_all_major, DecimalEncoder, get_all_class, get_all_type, is_login
from .models import MajorInfo, UserType, UserInfo, ClassInfo, Attendence, Notice, Leave, ExamContent, Exam
# django Self-contained encryption and decryption library
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q, Avg, Sum, Max, Min, Count
import hashlib
import json
import datetime
import pytz


# Create your views here.

# Check if the registered decorator
# def check_login(func):
#     def inner(request,*args,**kwargs):
#         (flag, rank) = check_cookie(request)
#         if flag:
#             func(request,*args,**kwargs)
#         else:
#             return render(request, 'page-login.html', {'error_msg': ''})
#
#     return inner

# Home
def index(request):
    return redirect('/check/')
    # (flag, rank) = check_cookie(request)
    # print('flag', flag)
    #
    # if flag:
    #     return render(request, 'check.html',locals())
    #
    # return render(request, 'page-login.html', {'error_msg': ''})


# Check-in statistics
@is_login
def total(request):
    (flag, user) = check_cookie(request)
    # if flag:
    if request.method == 'POST':
        nowdate = datetime.datetime.now()
        weekDay = datetime.datetime.weekday(nowdate)
        firstDay = nowdate - datetime.timedelta(days=weekDay)
        lastDay = nowdate + datetime.timedelta(days=6 - weekDay)
        # print(firstDay,lastDay)
        # info_list=Attendence.objects.filter(date__gte=firstDay,date__lte=lastDay).values('stu','stu__username','stu__cid__name').annotate(total_time=Sum('duration'),leave_count=Sum('is_leave')).order_by()
        info_list = Attendence.objects.filter(date__gte=firstDay, date__lte=lastDay).values('stu', 'stu__username',
                                                                                            'stu__cid__name',
                                                                                            'leave_count') \
            .annotate(total_time=Sum('duration')).order_by()
        info_list = json.dumps(list(info_list), cls=DecimalEncoder)

        return HttpResponse(info_list)
    else:
        nowdate = datetime.datetime.now()
        weekDay = datetime.datetime.weekday(nowdate)
        firstDay = nowdate - datetime.timedelta(days=weekDay)
        lastDay = nowdate + datetime.timedelta(days=6 - weekDay)
        # print(firstDay,lastDay)
        leave_list = Leave.objects.filter().values('user', 'start_time', 'end_time')
        # print(leave_list)
        info_list = Attendence.objects.filter(date__gte=firstDay, date__lte=lastDay).values('stu', 'stu__username',
                                                                                            'stu__cid__name',
                                                                                            'leave_count') \
            .annotate(total_time=Sum('duration')).order_by()

        # info_list=Attendence.objects.filter(date__gte=firstDay,date__lte=lastDay).values('stu','stu__username','stu__cid__name')\
        #     .annotate(total_time=Sum('duration'),leave_count=Sum('is_leave'))\
        #     .extra(
        #     select={'starttime':"select start_time from app_leave where %s BETWEEN start_time AND end_time"},
        #     select_params=[nowdate]
        # )\
        #     .order_by()

        # info_list=json.dumps(list(info_list),cls=DecimalEncoder)
        print(info_list)

        return render(request, 'total.html', locals())
    # else:
    #     return render(request, 'page-login.html', {'error_msg': ''})


#
# log in page
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        m1 = hashlib.sha1()
        m1.update(password.encode('utf8'))
        password = m1.hexdigest()
        print('password:', password)
        if check_login(email, password):
            response = redirect('/index/')
            response.set_cookie('qwer', email, 3600)
            response.set_cookie('asdf', password, 3600)
            return response
            # return HttpResponse('login successful')
        else:
            return render(request, 'page-login.html', {'error_msg': 'If the account number or password is incorrect, please re-enter'})
    else:
        (flag, rank) = check_cookie(request)
        print('flag', flag)
        if flag:
            return redirect('/index/')
        return render(request, 'page-login.html', {'error_msg': ''})


# registration page
@csrf_exempt
def register(request):
    if request.method == 'POST':
        if request.is_ajax():

            stu_num_v = request.POST.get('stu_num_verify')
            if UserInfo.objects.filter(studentNum=stu_num_v):
                ret = {'valid': False}
            else:
                ret = {'valid': True}

            return HttpResponse(json.dumps(ret))

    else:
        return render(request, 'register.html')


def check(request):
    (flag, rank) = check_cookie(request)
    # print('flag', flag)
    user = rank

    if flag:
        if request.method == 'POST':
            sign_flag = request.POST.get('sign')
            print('sign_flag', type(sign_flag), sign_flag)
            if sign_flag == 'True':
                Attendence.objects.create(stu=user, start_time=datetime.datetime.now())
            elif sign_flag == 'False':
                cur_attendent = Attendence.objects.filter(stu=user, end_time=None)
                tmp_time = datetime.datetime.now()
                duration = round((tmp_time - cur_attendent.last().start_time).seconds / 3600, 1)

                cur_attendent.update(end_time=tmp_time, duration=duration)
            return HttpResponse(request, 'Successful operation')
        else:
            # Query the status of the last check-in
            pre_att = Attendence.objects.filter(stu=user).order_by('id').last()
            # print(pre_att.end_time)
            if pre_att:
                # If the current time is more than six hours from the last check-in time, and the last check-out time is equal to the check-in time.
                if (datetime.datetime.now() - pre_att.start_time.replace(
                        tzinfo=None)).seconds / 3600 > 6 and pre_att.end_time == None:
                    # Attendence.objects.filter(stu=user, end_time=None).update(end_time=pre_att.start_time+datetime.timedelta(hours=2),duration=2,detail="自动签退")
                    pre_att.delete()
                    sign_flag = True

                elif (datetime.datetime.now() - pre_att.start_time.replace(
                        tzinfo=None)).seconds / 3600 < 6 and pre_att.end_time == None:
                    sign_flag = False
                else:
                    sign_flag = True
            else:
                sign_flag = True
            att_list = Attendence.objects.all().order_by('-id')

            return render(request, 'check.html', locals())

    return render(request, 'page-login.html', {'error_msg': ''})


# logout
def logout(request):
    req = redirect('/login/')
    req.delete_cookie('asdf')
    req.delete_cookie('qwer')
    return req


# Registration verification
def register_verify(request):
    if request.method == 'POST':
        print('Successful verification')
        username = request.POST.get('username')
        email = request.POST.get('email')
        stu_num = request.POST.get('stu_num')
        pwd = request.POST.get('password')
        m1 = hashlib.sha1()
        m1.update(pwd.encode('utf8'))
        pwd = m1.hexdigest()
        phone = request.POST.get('phone')
        a = UserInfo.objects.create(username=username, email=email, studentNum=stu_num, password=pwd,
                                    phone=phone, user_type_id=2)

        a.save()
        return HttpResponse('OK')


# Class management
def classManage(request):
    (flag, rank) = check_cookie(request)
    print('flag', flag)
    if flag:
        if rank.user_type.caption == 'admin':
            class_list = ClassInfo.objects.all()

            return render(request, 'classManage.html', {'class_list': class_list})
        else:
            return render(request, 'class_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# Edit class
@csrf_exempt
def edit_class(request):
    (flag, rank) = check_cookie(request)
    print('flag', flag)
    if flag:
        if rank.user_type.caption == 'admin':
            if request.method == 'POST':
                pre_edit_id = request.POST.get('edit_id')
                class_name = request.POST.get('edit_class_name')
                temp_flag = ClassInfo.objects.filter(name=class_name)
                print('pre_edit_id1', pre_edit_id)
                pre_obj = ClassInfo.objects.get(id=pre_edit_id)
                if not temp_flag and class_name:
                    pre_obj.name = class_name
                    pre_obj.save()
                return HttpResponse('Class modification succeeded')
            class_list = ClassInfo.objects.all()
            return render(request, 'classManage.html', {'class_list': class_list})
            # return HttpResponse('Edit class')
        else:
            return render(request, 'class_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


#
# Add class
@csrf_exempt
def add_class(request):
    # print('Come in')
    if request.method == 'POST':
        # print('this is post')
        add_class_name = request.POST.get('add_class_name')
        flag = ClassInfo.objects.filter(name=add_class_name)
        if flag:
            pass
            # print(' Existing data, not processed')
        else:
            if add_class_name:
                ClassInfo.objects.create(name=add_class_name).save()

        return HttpResponse('Add class success')


#Delete class
def delete_class(request):
    (flag, rank) = check_cookie(request)
    print('flag', flag)
    if flag:
        if rank.user_type.caption == 'admin':
            # class_list=ClassInfo.objects.all()
            delete_id = request.GET.get('delete_id')
            ClassInfo.objects.filter(id=delete_id).delete()
            return redirect('/classManage/')
        else:
            return render(request, 'class_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# Professional management
def majorManage(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            major_list = MajorInfo.objects.all()

            return render(request, 'major_manage.html', {'major_list': major_list})
        else:
            return render(request, 'major_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# Add professional
@csrf_exempt
def add_major(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            major_list = MajorInfo.objects.all()
            if request.method == 'POST':

                add_major_name = request.POST.get('add_major_name')
                print(add_major_name)
                if not MajorInfo.objects.filter(name=add_major_name):
                    new_major = MajorInfo.objects.create(name=add_major_name)
                return HttpResponse('Professionally added successfully')

            return render(request, 'major_manage.html', {'major_list': major_list})
        else:
            return render(request, 'major_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# Delete professional
def delete_major(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':

            delete_major_id = request.GET.get('delete_id')
            MajorInfo.objects.get(id=delete_major_id).delete()
            major_list = MajorInfo.objects.all()
            return render(request, 'major_manage.html', {'major_list': major_list})
        else:
            return render(request, 'major_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


#
# Editorial profession
@csrf_exempt
def edit_major(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            major_list = MajorInfo.objects.all()
            edit_major_id = request.POST.get('edit_major_id')
            edit_major_name = request.POST.get('edit_major_name')
            print(edit_major_id)
            print(edit_major_name)
            if not MajorInfo.objects.filter(name=edit_major_name):
                change_obj = MajorInfo.objects.get(id=edit_major_id)
                change_obj.name = edit_major_name
                change_obj.save()
            return HttpResponse('Professional revision success')

        else:
            return render(request, 'major_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


#
# Member management
def member_manage(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            member_list = UserInfo.objects.all()

            return render(request, 'member_manage.html', {'member_list': member_list})
        else:
            return render(request, 'member_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


# Delete member
def delete_member(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            delete_sno = request.GET.get('delete_sno')
            UserInfo.objects.get(studentNum=delete_sno).delete()
            member_list = UserInfo.objects.all()
            return render(request, 'member_manage.html', {'member_list': member_list})
        else:
            return render(request, 'member_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


#
# Edit member
def edit_member(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':

            if request.method == 'POST':
                student_num = request.POST.get('student_num')
                username = request.POST.get('username')
                email = request.POST.get('email')
                age = request.POST.get('age')
                if age:
                    age = int(age)
                else:
                    age = 0

                gender = int(request.POST.get('gender'))
                cls = ClassInfo.objects.get(name=request.POST.get('cls'))
                nickname = request.POST.get('nickname')
                usertype = UserType.objects.get(caption=request.POST.get('user_type'))
                phone = request.POST.get('phone')
                motto = request.POST.get('motto')
                edit_obj = UserInfo.objects.filter(studentNum=student_num)
                edit_obj.update(studentNum=student_num, username=username, email=email, cid=cls, nickname=nickname,
                                user_type=usertype, motto=motto,
                                gender=gender, phone=phone,
                                age=age
                                )
                member_list = UserInfo.objects.all()

                return redirect('/memberManage/', {'member_list': member_list})
            else:
                edit_member_id = request.GET.get('edit_sno')
                #
                # List of all user types
                stu_type_list = UserType.objects.all()
                # All classes
                cls_list = ClassInfo.objects.all()
                #
                # All professions
                major_list = MajorInfo.objects.all()
                # Currently edited user object
                edit_stu_obj = UserInfo.objects.get(studentNum=edit_member_id)
                return render(request, 'edit_member.html', locals())
        else:
            return render(request, 'member_manage_denied.html')
    else:
        return render(request, 'page-login.html', {'error_msg': ''})


#Announcement wall display
@is_login
def notice(request):
    info_list = Notice.objects.all().order_by('-post_date')
    return render(request, 'notice.html', locals())


# Announcement wall release
@is_login
def noticeManage(request):
    (flag, user) = check_cookie(request)
    if user.user_type.caption == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            level = request.POST.get('selectLevel')
            Notice.objects.create(head=title, content=content, level=level, author=user)
            return render(request, 'notice_manage.html')
        else:
            return render(request, 'notice_manage.html')
    else:
        return render(request, 'notice_manage_denied.html')


# Leave management
@is_login
def leave(request):
    (flag, user) = check_cookie(request)
    leave_list = Leave.objects.all()
    if request.method == 'POST':
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        print(starttime)
        a = int(datetime.datetime.strptime(starttime, '%Y-%m-%d').day - datetime.datetime.strptime(endtime,
                                                                                                   '%Y-%m-%d').day) + 1
        explain = request.POST.get('explain')
        Leave.objects.create(start_time=starttime, end_time=endtime, user=user, explain=explain)
        Attendence.objects.filter(date__gte=starttime, date__lte=endtime, stu=user).update(
            leave_count=F('leave_count') + a)
    return render(request, 'leave.html', locals())


# Assessment record
@is_login
def exam(request):
    exam_list=ExamContent.objects.all()
    exam_id=request.GET.get('exam_id')
    if exam_id:
        user_list=Exam.objects.filter(content_id=exam_id).all()
    return render(request, 'exam.html',locals())


#
# Assessment management
@is_login
def exam_manage(request):
    (flag, user) = check_cookie(request)
    if user.user_type.caption == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')

            if title:
                ExamContent.objects.create(title=title)
            else:
                count = UserInfo.objects.all().count()
                content_id = request.POST.get('exam_id')
                for i in range(count):
                    point=request.POST.get('point{}'.format(i))

                    stuID=request.POST.get('stu{}'.format(i))
                    detail = request.POST.get('detail{}'.format(i))
                    Exam.objects.create(point=point,content_id=content_id,user_id=stuID,detail=detail)
                # print(request.body)
                ExamContent.objects.filter(id=content_id).update(state=True)
        check_list = ExamContent.objects.filter(state=False)
        user_list = UserInfo.objects.all()
        return render(request, 'exam_manage.html', locals())
    else:
        return render(request, 'exam_manage_denied.html')
