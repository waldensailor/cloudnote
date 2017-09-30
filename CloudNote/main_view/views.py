from main_view.models import Article
from main_view.models import Tag
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from datetime import *
import time
from django.db.models import Count
import re
import os, base64


# Create your views here.


# 设置全局变量：图片路径和格式
def gobal_setting(request):
    return {'IMG_PATH': settings.IMG_PATH, 'IMG_TYPE': settings.IMG_TYPE}


# 格式化时间为datetime类型
def bz_time(string):
    return datetime.strptime(string, "%Y年%m月%d日 %H:%M:%S")


# 注册处理结果
def regist_deal(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    name = request.POST.get('name', '')
    # 查询数据库，改邮箱是否已经注册，如果注册则返回当前页面
    regist_user = User.objects.filter(username=name)# 查询该邮件是否已经注册
    # 记录是否注册的状态
    regist_info = "该用户已注册，请更换用户名"
    if regist_user:
       # 已经注册
        return render(request, "main_view/registeration.html", {"user_data": regist_info})
    else:
        # 现在注册
        regist_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            User.objects.create_user(email=email, password=password, username=name, date_joined=regist_time)
        except:
            print("插入数据出错")
            regist_info = "服务器正在维护，请稍后再试"
            return render(request, "main_view/registeration.html", {"user_data": regist_info})
        regist_info = "恭喜你注册成功，请转到登陆"
        return render(request, "main_view/registeration.html", {"user_data": regist_info})


# 返回注册界面
def return_regist(request):
    return render(request, "main_view/registeration.html")


# 注销账户
def return_logout(request):
    auth.logout(request)
    tip_data = [{"tip_message": "dl"},
                ]
    return render(request, "main_view/login.html", {"tip_data": tip_data})


# 返回登陆界面
def return_login(request):
    tip_data = [{"tip_message": "dl"},
                ]
    return render(request, "main_view/login.html", {"tip_data": tip_data})


# 登陆的检测函数，主界面的入口函数
def index(request):
    # email = request.POST.get('email', '')
    # password = request.POST.get('password', '')
    # if email and password:
    #     login_user = User.objects.filter(email=email).filter(password=password)
    #     if login_user:
    #         # 登陆成功并且跳转
    #         for abc in login_user:
    #             print("name:", abc.user_name)
    #         return render(request, "main_view/index.html", {"user_data": login_user[0]})
    #     else:
    #         tip_data = [{"tip_message": "提示：邮箱或密码错误"},
    #                     ]
    #         return render(request, "main_view/login.html", {"tip_data": tip_data})
    #         # 邮箱或密码错误
    # else:
    #     tip_data = [{"tip_message": "提示：邮箱和密码均不可为空"},
    #                 ]
    #     return render(request, "main_view/login.html", {"tip_data": tip_data})
    #     # 用户密码必须都不为空
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if email and password:
        print(email, password)
        user = authenticate(username=email, password=password)
        print(type(user))
        if user is not None and user.is_active:
            # 登陆成功并且跳转
            auth.login(request, user)
            login_user = User.objects.filter(username=email)
            return render(request, "main_view/index.html", {"user_data": login_user[0]})
        else:
            tip_data = [{"tip_message":"提示：用户名或密码错误,或该用户已在线"},
            ]
            return render(request, "main_view/login.html", {"tip_data": tip_data})
    else:
        tip_data = [{"tip_message": "提示：用户名和密码均不可为空"},
                    ]
        return render(request, "main_view/login.html", {"tip_data": tip_data})


# 返回查看用户所有笔记
def return_readmore(request):
    all_article = Article.objects.filter(user_id=request.user.id).order_by("-id").defer('content')
    all_tags = Tag.objects.filter(user_id=request.user.id)
    return render(request, "main_view/readmore.html", {"article": all_article, "tags": all_tags})


# 编辑页面
def return_editor(request):
    return render(request, "main_view/editor.html")


# 笔记存储处理
def editor_storage(request):
    if request.method == "POST":
        note_title = request.POST["note_title"]
        note_content = request.POST["note_content"]
        note_tags = request.POST["note_tags"]
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        try:
            Article.objects.create(user_id=request.user.id, title=note_title, content=note_content, create_time=create_time, last_time=create_time)
            # 标签部位空则执行操作
            if len(note_tags) != 0:
                # 获取这篇文章的id,因为原来个是[{"x":x,"y":y},]
                this_article = Article.objects.filter(user_id=request.user.id, create_time=create_time)
                this_article_id = this_article[0].id
                tags_list = re.split(r"[；;,，: ：]", note_tags)
                tags_list = list(set(tags_list))
                print(tags_list)
                for tag_i in tags_list:
                    # 排除空的tag
                    if tag_i != "":
                        Tag.objects.create(user_id=request.user.id, user_article_id=this_article_id, tag=tag_i)
            return HttpResponse("保存成功")
            # return render(request, "main_view/editor.html")
        except:
            return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护")
    else:
        return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护")


# 查看笔记详细，并进入read_article页面并可以编辑
def read_article(request):
    if request.method == "GET":
        try:
            article_id = request.GET["article_id"]
            # 简单的查询，没什么好说的
            this_article = Article.objects.get(id=article_id)
            all_tags = Tag.objects.filter(user_article_id=article_id)
            tag_text = ""
            for tag in all_tags:
                tag_text = tag_text + tag.tag + ";"
            return render(request, "main_view/read_article.html", {"article": this_article, "tags": tag_text})
        except:
            return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护")
    else:
        return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护")


# 笔记编辑更新函数
def article_update(request):
    if request.method == "POST":
        try:
            article_id = request.POST["article_id"]
            note_title = request.POST["note_title"]
            note_content = request.POST["note_content"]
            note_tags = request.POST["note_tags"]
             # 修改文章tag
            Tag.objects.filter(user_article_id=article_id).delete()# 废旧立新tags
            # 当新的标签组不为空则切割，去重
            if len(note_tags) != 0:
                tags_list = re.split(r"[；;,，||:：]", note_tags)
                tags_list = list(set(tags_list))
                for tag_i in tags_list:
                    # 排除tag为空的函数
                    if tag_i != "":
                        Tag.objects.create(user_id=request.user.id, user_article_id=article_id, tag=tag_i)
            # 修改文章
            last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            Article.objects.filter(id=article_id).update(title=note_title, content=note_content, last_time=last_time)
            return HttpResponse("更新成功！！")
        except:
            return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护1")
    else:
        return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护1")


# 笔记删除函数
def delete_article(request):
    if request.method == "POST":
        article_id = request.POST["article_id"]
        try:
            Article.objects.filter(id=article_id).delete()
            Tag.objects.filter(user_article_id=article_id).delete()
            return HttpResponse("删除成功")
        except:
            return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护")
    else:
        return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护")


# 返回个人信息页面
def return_aboutme(request):
    return render(request, "main_view/aboutme.html")


def return_test(request):
    return render(request, "main_view/test1.html")


# 返回查询笔记页面
def search_article(request):
    return render(request, "main_view/search_article.html")


# 返回标签管理页面
def tag_manage(request):
    try:
        all_tags = Tag.objects.filter(user_id=request.user.id).values("tag").annotate(count=Count("tag")).values('tag', 'count')
    except:
        return HttpResponse("由于不可描述的原因，标签暂无法获取，工程师正在维护")
    return render(request, "main_view/tag_manage.html", {"all_tags": all_tags})


# 返回个人信息页面
def about_me(request):
    return render(request, "main_view/aboutme.html")


# 修改个人信息
def me_update(request):
    if request.method == "POST":
        try:
            # 获取新的消息
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            # 修改信息
            has_user = User.objects.filter(username=username)
            username_me = User.objects.get(id=request.user.id).username
            if username != username_me:
                if has_user:
                    return HttpResponse("该username已经被占用，请重新设置")
            User.objects.filter(id=request.user.id).update(username=username, first_name=first_name, email=email, last_name=last_name)
            return HttpResponse("更新成功！！")
        except:
            return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护1")
    else:
        return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护1")


# 修改密码
def change_password(request):
    if request.method == "POST":
        try:
            password = request.POST["password"]
            # 检验老密码是否正确
            user = authenticate(username=request.user.username, password=password)
            if user:
                new_password = request.POST["new_password"]
                # 老密码正确，修改
                user.set_password(new_password)
                user.save()
                return HttpResponse("修改密码成功,请重新登陆")
            else:
                return HttpResponse("原密码输入不正确")
        except:
            return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护1")
    else:
        return HttpResponse("由于不可描述的原因，没有保存成功，工程师正在维护1")


# 删除标签
def delete_tag(request):
    if request.method == "POST":
        try:
            tag = request.POST["tag"]
            # 删除操作
            Tag.objects.filter(user_id=request.user.id, tag=tag).delete()
        except:
            return HttpResponse("由于不可描述的原因，没有删除存成功，工程师正在维护1")
        return HttpResponse("删除标签成功")
    else:
        return HttpResponse("由于不可描述的原因，没有删除成功，工程师正在维护1")


# 修改标签
def update_tag(request):
    if request.method == "POST":
        try:
            old_tag = request.POST["old_tag"]
            new_tag = request.POST["new_tag"]
            # 更新操作
            Tag.objects.filter(tag=old_tag, user_id=request.user.id).update(tag=new_tag)
        except:
            return HttpResponse("由于标签太调皮，修改失败，不过工程师正在维护")
        return HttpResponse("标签修改成功")
    else:
        return HttpResponse("由于标签太调皮，修改失败，不过工程师正在维护")


# 更据标签查找笔记：
def search_from_tag(request):
    # 定义一个文章id列表，用于存放最终目的文章id
    article_list = []
    if request.method == "POST":
        try:
            search_tags = request.POST.get("search_tags","")
            search_type = request.POST.get("search_type","")
            # 获取tags,切割，去空
            tags_list = re.split(r"[;；，。：:|. ,]", search_tags)
            tags_list = list(set(tags_list))
            for i in tags_list:
                if i == "":
                    tags_list.remove(i)
            # 并查询
            if search_type == "and":
                # 获取列表的长度
                tag_number = len(tags_list)
                # 筛选该用户的所有笔记，笔记标签任一符合的都选中，按照选中的文章id分类查数量，返回id和符合的tag个数
                try:
                    tag_count_list = Tag.objects.filter(user_id=request.user.id, tag__=tags_list).values("user_article_id").annotate(count=Count("user_article_id")).values_list("user_article_id", "count")
                except:
                    return HttpResponse("你输入了不存在的标签")
                for tag_count in tag_count_list:
                    if tag_count[1] == tag_number:
                        article_list.append(tag_count[0])
            # 或查询
            elif search_type == "or":
                article_id_list = Tag.objects.filter(user_id=request.user.id, tag__in=tags_list).values_list('user_article_id').distinct()
                for this_article_tuble in article_id_list:
                    article_list.append(this_article_tuble[0])
                # 查找这些文章
            if len(article_list)==0:
                return HttpResponse("君上，符合条件的笔记没有诶，要不再核对一下")
            article_result = Article.objects.filter(id__in=article_list).defer("content")
            # 查找标签
            all_tags = Tag.objects.filter(user_id=request.user.id, tag__in=tags_list).defer("id", "user_id")
            return render(request, "main_view/readmore.html", {"article": article_result, "tags": all_tags})
        except:
            return HttpResponse("由于标签太调皮，查询没有结果")
    # 从标签管理页面传过来的用的是GET方法
    elif request.method == "GET":
        # 获取传过来的标签
        search_tag = request.GET.get("tag", "")
        try:
            # 更具标签查询笔记id的列表-列表
            article_id_list = Tag.objects.filter(user_id=request.user.id, tag=search_tag).values_list('user_article_id').distinct()
            # 吧[[1],[2],]酱紫的列表改成[2,1,]
            for this_article_tuble in article_id_list:
                article_list.append(this_article_tuble[0])
            # 查询笔记和标签
            article_result = Article.objects.filter(id__in=article_list).defer("content")
            all_tags = Tag.objects.filter(user_id=request.user.id).defer("id", "user_id")
            return render(request, "main_view/readmore.html", {"article": article_result, "tags": all_tags})
        except:
            return HttpResponse("这个标签跑丢了，洒家还没找到他")
    else:
        return HttpResponse("由于标签太调皮，查找失败，查询没有结果")


# 更据内容查找笔记：
def search_from_content(request):
    if request.method == "POST":
        try:
            # 获取查询条件
            title_some = request.POST.get("title_some", "")
            content_some = request.POST.get("content_some", "")
            create_time_1 = request.POST.get("create_time_1", "")
            create_time_2 = request.POST.get("create_time_2", "")
            last_time_1 = request.POST.get("last_time_1", "")
            last_time_2 = request.POST.get("last_time_2", "")
            # 将字符串型的时间格式化成datetime类型才能与数据中的时间比较
            create_time_l = bz_time(create_time_1)
            create_time_u = bz_time(create_time_2)
            last_time_l = bz_time(last_time_1)
            last_time_u = bz_time(last_time_2)
            # 检测时间区间是否合法
            if create_time_l >= create_time_u:
                return HttpResponse("创建笔记时间的范围不正确")
            if last_time_l >= last_time_u:
                return HttpResponse("最后修改的时间区间不正确")
            # z针对查询条件是否为空执行不同的条件语句
            if title_some != "":
                # 标题和内容都不为空
                if content_some != "":
                    # 天呐撸，一个时间区间竟然要写成两条条件来查找
                    article_result = Article.objects.filter(user_id=request.user.id, title__contains=title_some, \
                                           content__contains=content_some, create_time__gte=create_time_l,\
                                           create_time__lte=create_time_u ,last_time__lte=last_time_u, last_time__gte=last_time_l)
                # 标题不为空，内容为空
                else:
                    article_result = Article.objects.filter(user_id=request.user.id, title__contains=title_some, \
                                                            create_time__gte=create_time_l, create_time__lte=create_time_u, \
                                                            last_time__lte=last_time_u, last_time__gte=last_time_l)
            else:
                # 标题为空，内容不为空
                if content_some!="":
                    article_result = Article.objects.filter(user_id=request.user.id, content__contains=content_some, \
                                                            create_time__gte=create_time_l, create_time__lte= \
                                                                create_time_u, last_time__lte=last_time_u, last_time__gte=last_time_l)
                # 标题为空，内容为空
                else:
                    article_result = Article.objects.filter(user_id=request.user.id, create_time__gte=create_time_l, \
                                                            create_time__lte=create_time_u, last_time__lte=last_time_u, last_time__gte=last_time_l)

            if len(article_result)==0:
                return HttpResponse("君上，符合条件的笔记没有诶，要不再核对一下")
            # 获取标签，模板需要用到
            all_tags = Tag.objects.filter(user_id=request.user.id).defer("id", "user_id")
            return render(request, "main_view/readmore.html", {"article": article_result, "tags": all_tags})
        except:
            return HttpResponse("君上，您的操作姿势不正确，在核对一下吧！")
        # 返回数据
        return
    else:
        return HttpResponse("请仔细核对内容")


# 更换头像
def img_update(request):
    img_str = request.POST.get("image", "")
    img_str = img_str[22:]
    print(img_str)
    # img_data = decode_base64(img_str.encode())
    # img_data = decode_base64(img_str)
    img_data = img_str.encode()
    print("aha")

    file = open('xiayimin.jpg', 'wb')
    # 需要字节类型的数据而不是str
    file.write(img_str)
    print("dafdsafdf")
    file.close()
    return HttpResponse("请仔细核对内容")


def decode_base64(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.decodestring(data)

def shuchu():
    return HttpResponse("看来释怀了")