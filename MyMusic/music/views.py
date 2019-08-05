import csv
import hashlib
import time,json
import traceback

from django.shortcuts import render, render_to_response, reverse, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import MusicStyle, MusicLanguage, SongList, Music, MV, User, Admin
from .my_tools import song, song_list, list_songs, get_list_music, search_music, get_music_info,paihang,mv
from .my_tools import encrypt, verification
from .forms import MyForm
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage     # 分页
from django.db.models import Q
# Create your views here.


# class Login(View):
#     def get(self, request):
#         return render(request, "login.html")
#
#     def post(self, request):
#         form = MyForm(request.POST)
#         if form.is_valid():
#             email =form.cleaned_data.get('username')
#             print(email)
#             return HttpResponse('验证成功')
#         else:
#             print("不是邮箱。。。")
#             return HttpResponse("验证失败")


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        username = username.strip()
        password = password.strip()

        if username == "" or username == "username" or password == "" or password == "password":
            return render(request, 'login.html', context={'context': "请输入用户名或密码!!!"})

        else:
            password = encrypt.md5_encrypt(password)
            print(username, password)

            try:
                user = User.objects.get(Q(username__icontains=username) | Q(email__icontains=encrypt.md5_encrypt(username)))
                if user.password == password:
                    # return render(request, 'index.html')

                    # 设置cookie
                    response = HttpResponseRedirect(reverse('index'))
                    response.set_cookie('username', username)
                    response.cookies.get('username')

                    return response
                else:
                    return render(request, 'login.html', context={"context": "密码错误！！！"})
            except:
                # 用户不存在
                return render(request, 'login.html', context={'context': "用户名不存在！！！"})


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        username = username.strip()
        password = password.strip()
        email = email.strip()

        # 若查询到，说明此用户已经注册过
        # username_select = User.objects.filter(username__exact=username)
        username_select = User.objects.filter(
            Q(username__icontains=username) | Q(email__icontains=encrypt.md5_encrypt(email)))
        print(username_select, len(username_select))

        if len(username_select) != 0:
            return render(request, 'register.html', context={'context': "用户名或邮箱已存在！！！"})
        else:
            if password != "password" and password != "" \
                    and username != "username" and username != ""\
                    and email != "email address" and email != "":
                # 使用md5加密函数
                password = encrypt.md5_encrypt(password)

                # 验证邮箱
                back_result = verification.verification(email)  # 邮箱验证结果
                if back_result == 'error':
                    return render(request, 'register.html', context={"context": "请输入正确的邮箱地址"})
                email = encrypt.md5_encrypt(email)
                print(password, email)
                user = User(username=username, password=password, email=email)

                user.save()

                return redirect(reverse('login'))
            elif username == "" or username == "username":
                # return redirect(reverse('register'))
                return render(request, 'register.html', context={"context": "用户名不能为空！！！"})
            elif email == "" or email == "email address":
                return render(request, 'register.html', context={"context": "邮箱不能为空!!!"})
            elif password == "" or password == "password":
                return render(request, 'register.html', context={"context": "密码不能为空!!!"})


def index(request):
    cookie = request.COOKIES.get('username')
    #
    # print(cookie)


    sing_list_info = SongList.objects.all().values_list('list_title', 'list_img', 'list_id')
    # print(sing_list_info)
    song_info = []
    for i in sing_list_info[60:76]:
        song_info.append({'list_title': i[0], 'list_img': i[1], 'list_id': int(i[2])})

    mv_info = []
    mv_list_info = MV.objects.all().values('mv_id', 'mv_name', 'mv_author', 'mv_pic', 'playCount', 'publishTime')
    for i in mv_list_info[3:9]:
        mv_info.append(i)

    context = {
        'infos': song_info,
        'mv_infos': mv_info,
        "username": cookie
    }

    return render(request, 'index.html', context=context)


def rotate_view(request, rotate_id):
    # 检查cookie
    cookie = request.COOKIES.get('username')
    print(cookie)
    if cookie is None:
        return redirect(reverse('login'))

    return render(request, 'rotate.html', context={"id": rotate_id})


def song_list_detail(request, songlist_id):     # 此参数要与url中的名字一致
    """ 列表详情 """
    print(songlist_id)

    # 检查cookie
    cookie = request.COOKIES.get('username')
    print(cookie)
    if cookie is None:
        return redirect(reverse('login'))

    songlist_info = SongList.objects.filter(list_id__exact=songlist_id).values('id', 'list_title', 'list_img', 'list_tag')

    list_info = songlist_info[0]

    id = list_info.get('id')
    list_title = list_info.get('list_title')
    list_img = list_info.get('list_img')
    list_tag = list_info.get('list_tag').split(" ")
    list_tags = []
    for i in list_tag:
        list_tags.append(i)

    music_infos = Music.objects.filter(music_list_id__exact=id).values('music_name', 'music_author', 'music_album', 'music_id', "music_img")
    # print(music_infos)
    context = {
        "list_title": list_title,
        "list_img":list_img,
        "list_tags": list_tags,
        "music_infos": music_infos,
    }

    return render(request, 'song_list_detail.html',context=context)


def recommend(request):
    """ 推荐 """
    return render(request, 'recommend.html')

def songlist(request):
    """ 歌单 """

    # # 检查cookie
    # cookie = request.COOKIES.get('username')
    # print(cookie)
    # if cookie is None:
    #     return redirect(reverse('login'))

    list = SongList.objects.all().values('list_id', 'list_title', 'list_img', 'list_tag')

    print(list) # [{},{},{}...]

    limit = 20
    # 将数据进行分页
    paginator = Paginator(list, limit)  # 按每页20条数据
    if request.method == "GET":

        page = request.GET.get('page')  # 默认跳转到第一页
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except InvalidPage:
            return HttpResponse("找不到页面内容")
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

    return render(request, 'songlist.html', context={"contexts": result})


def list(request):
    """ 榜单 """

    cookie = request.COOKIES.get('username')
    print(cookie)
    if cookie is None:
        return redirect(reverse('login'))

    list = paihang.get_paihang()

    limit = 10
    # 将数据进行分页
    paginator = Paginator(list, limit)  # 按每页20条数据
    if request.method == "GET":
        
        page = request.GET.get('page')  # 默认跳转到第一页
        try:
            infos = paginator.page(page)
        except PageNotAnInteger:
            infos = paginator.page(1)
        except InvalidPage:
            return HttpResponse("找不到页面内容")
        except EmptyPage:
            infos = paginator.page(paginator.num_pages)

    # {'infos':[{},{},{},{}...]}
    return render(request, 'list.html', context={"infos": infos})


def MV_view(request):
    """ MV """
    # list = mv.get_mv()  # [{},{},{},{}...]
    list = MV.objects.all()  # [{},{},{},{}...]

    limit = 12
    # 将数据进行分页
    paginator = Paginator(list, limit)  # 按每页20条数据
    if request.method == "GET":

        page = request.GET.get('page')  # 默认跳转到第一页
        try:
            mv_infos = paginator.page(page)
        except PageNotAnInteger:
            mv_infos = paginator.page(1)
        except InvalidPage:
            return HttpResponse("找不到页面内容")
        except EmptyPage:
            mv_infos = paginator.page(paginator.num_pages)

    return render(request, 'mv.html', context={'mv_infos':mv_infos})


def mv_detail(request, mv_id):
    print(mv_id)

    # 检查cookie
    cookie = request.COOKIES.get('username')
    print(cookie)
    if cookie is None:
        return redirect(reverse('login'))


    result = MV.objects.filter(mv_id=mv_id)
    print(result)

    context = {
        "result": result,
        "mv_url":mv.get_mv_url(mv_id)
    }

    return render(request, 'mv_detail.html', context=context)


def search(request):
    """ 搜索 """

    # 检查cookie
    cookie = request.COOKIES.get('username')
    print(cookie)
    if cookie is None:
        return redirect(reverse('login'))

    if request.method == "GET":
        return render(request, 'index.html')
    if request.method == "POST":

        web = {'netease': "网易云音乐", 'qq': "QQ音乐", "kugou": "酷狗音乐", 'kuwo':"酷我",
               'migu': "咪咕", 'lizhi':"荔枝", 'xiami': "虾米"}

        search_name = request.POST.get('search_music')
        search_website = request.POST.get('website')

        # print(search_name, search_website)

        result = search_music.search(search_website, search_name)

        print(result)
        context = {
            "search_website": web.get(search_website),
            'search_name': search_name,
            'result': result
        }

        return render(request, 'search.html', context=context)


def admin(request):
    if request.method == "GET":
        return render(request, 'admin.html')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        username = username.strip()
        password = encrypt.md5_encrypt(password.strip())

        if username == "" or username == "username or email" or \
                password == "" or password == "password":
            return render(request, 'admin.html', context={'context': "请输入！！！"})


        try:
            a_user = Admin.objects.get(username__exact=username)

            if a_user.password == password:

                # 设置cookie
                response = HttpResponseRedirect("/admin_music")
                response.set_cookie('admin_username', username)

                # return redirect(reverse('admin_music'))
                return response
            else:
                return render(request, 'admin.html', context={"context": "密码错误！！！"})
        except:
            return render(request, 'admin.html', context={'context': "此管理员不存在！！！"})





def admin_music(request):
    if request.method == "GET":

        # 检查cookie
        cookie = request.COOKIES.get('admin_username')
        print(cookie)
        if cookie is None:
            return redirect(reverse('admin'))

        list = Music.objects.all().values('music_id', 'music_name', 'music_author', 'music_album')
        # print(list)

        limit = 20
        # 将数据进行分页
        paginator = Paginator(list, limit)  # 按每页20条数据
        if request.method == "GET":

            page = request.GET.get('page')  # 默认跳转到第一页
            try:
                result = paginator.page(page)
            except PageNotAnInteger:
                result = paginator.page(1)
            except InvalidPage:
                return HttpResponse("找不到页面内容")
            except EmptyPage:
                result = paginator.page(paginator.num_pages)

        return render(request, 'admin_music.html', context={'result': result})

    if request.method == "POST":
        # 点击退出
        if request.POST.get("exit"):
            # request.COOKIES.clear()     # 退出删除cookie
            # request.COOKIES = None
            # return redirect(reverse('index'))
            response = HttpResponseRedirect(reverse('index'))
            response.delete_cookie('admin_username')
            return response

        # 删除信息
        m_id = request.POST.get('m_id')
        print(m_id)
        music = Music.objects.filter(music_id=m_id)
        music[0].delete()
        print(music[0])

        # return render(request, 'admin_music.html')
        return redirect(reverse('admin_music'))


def admin_user(request):
    if request.method == "GET":

        # 检查cookie
        cookie = request.COOKIES.get('admin_username')
        print(cookie)
        if cookie is None:
            return redirect(reverse('admin'))

        list = User.objects.all().values('username', 'password', 'email')
        # print(list)

        limit = 20
        # 将数据进行分页
        paginator = Paginator(list, limit)  # 按每页20条数据
        if request.method == "GET":

            page = request.GET.get('page')  # 默认跳转到第一页
            try:
                result = paginator.page(page)
            except PageNotAnInteger:
                result = paginator.page(1)
            except InvalidPage:
                return HttpResponse("找不到页面内容")
            except EmptyPage:
                result = paginator.page(paginator.num_pages)
        return render(request, 'admin_user.html', context={'result': result})

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        result = User.objects.get(username__exact=username, password__exact=password)
        result.delete()

        return redirect(reverse('admin_user'))


def admin_mv(request):
    if request.method == "GET":

        # 检查cookie
        cookie = request.COOKIES.get('admin_username')
        print(cookie)
        if cookie is None:
            return redirect(reverse('admin'))

        list = MV.objects.all().values('mv_id', 'mv_name', 'mv_author', 'mv_pic', "playCount", 'publishTime')
        # print(list)

        limit = 20
        # 将数据进行分页
        paginator = Paginator(list, limit)  # 按每页20条数据
        if request.method == "GET":

            page = request.GET.get('page')  # 默认跳转到第一页
            try:
                result = paginator.page(page)
            except PageNotAnInteger:
                result = paginator.page(1)
            except InvalidPage:
                return HttpResponse("找不到页面内容")
            except EmptyPage:
                result = paginator.page(paginator.num_pages)
        return render(request, 'admin_mv.html', context={'result': result})

    if request.method == "POST":
        mv_id = request.POST.get('mv_id')
        result = MV.objects.filter(mv_id=mv_id)
        result[0].delete()

        return redirect(reverse('admin_mv'))


def test(request):

    # # 分页
    #     # book_list = []
    #     # '''
    #     # 数据通常是从 models 中获取。这里为了方便，直接使用生成器来获取数据。
    #     # '''
    #     # for x in range(1, 26):  # 一共 25 本书
    #     #     book_list.append('Book ' + str(x))
    #     #
    #     # # 将数据按照规定每页显示 10 条, 进行分割
    #     # paginator = Paginator(book_list, 10)
    #     #
    #     # if request.method == "GET":
    #     #     # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    #     #     page = request.GET.get('page')
    #     #     try:
    #     #         books = paginator.page(page)
    #     #     # todo: 注意捕获异常
    #     #     except PageNotAnInteger:
    #     #         # 如果请求的页数不是整数, 返回第一页。
    #     #         books = paginator.page(1)
    #     #     except InvalidPage:
    #     #         # 如果请求的页数不存在, 重定向页面
    #     #         return HttpResponse('找不到页面的内容')
    #     #     except EmptyPage:
    #     #         # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
    #     #         books = paginator.page(paginator.num_pages)
    #     #
    #     # template_view = 'test.html'
    # return render(request, template_view, {'books': books})



    # response = HttpResponse('ok')
    # response.set_cookie('cookie', '你好哇')
    #
    # cookie = response.cookies.get('cookie')
    #
    # print(cookie)
    #
    # return HttpResponse(cookie)
    username = "123"
    password = '456'
    response = render_to_response('test.html', {})
    response.set_cookie('username', username,'passwd',password)
    cookie = response.cookies.get('username', 'password')
    print(cookie)
    return HttpResponse(cookie)



def get_data(request):
    """ 爬取网易云音乐数据视图 """
    # # 风格，保存到数据库
    # style = song_list.run().get("music_style")
    # for i in style:
    #     MusicStyle(style=i).save()


    # # 语种，保存到数据库
    # style = song_list.run().get("music_language")
    # for i in style:
    #     MusicLanguage(language=i).save()
    #
    # return HttpResponse("ojbk")


    # # 歌单
    # song_list_data = song_list.run()    # 调用爬虫
    #
    # for li in song_list_data:
    #     list_id = li.get('list_id')
    #     list_title = li.get('list_title')
    #     list_img = li.get('list_img')
    #     list_tag = li.get('list_tag')
    #
    #     print("正在存储",list_id, list_title, list_img, list_tag)
    #
    #     song_tag = SongList(
    #         list_id=list_id,
    #         list_title=list_title,
    #         list_img=list_img,
    #         list_tag=list_tag
    #     )
    #
    #     tag_list = list_tag.split(" ")
    #
    #     # # 此条数据在数据库中知否存在
    #     # check = SongList.objects.filter(list_id__exact=list_id)
    #
    #     for tag in tag_list:
    #         # 获取style和language的id
    #         get_style_id = MusicStyle.objects.filter(style__contains=tag).values('id')
    #         get_language_id = MusicLanguage.objects.filter(language__contains=tag).values('id')
    #
    #         # 检查此条数据在数据库中是否已存在
    #         check = SongList.objects.filter(list_id__exact=list_id)
    #
    #         if len(check) == 0:     # 若数据库中不存在，则添加此条数据
    #             if len(get_style_id) != 0:      # 若在MusicStyle找到此tag，则使用MusicStyle添加数据
    #                 try:
    #                     music_type = MusicStyle.objects.get(style__exact=tag)
    #                 except:
    #                     pass
    #             elif len(get_language_id) != 0:   # 若在MusicLanguage中找到此tag，则使用MusicLanguage添加数据
    #                 try:
    #                     music_type = MusicLanguage.objects.get(language__exact=tag)
    #                 except:
    #                     pass
    #             else:
    #                 print("没有此标签：", tag)
    #
    #             # try:
    #             #     music_type = MusicStyle.objects.get(style__exact=tag)   # 使用get如找不到会报错，即：没有此条数据
    #             # except:
    #             #     music_type = MusicLanguage.objects.get(language__exact=tag)
    #             # finally:
    #             #     print("没有此标签：", tag)
    #
    #             music_type.songlist_set.add(song_tag, bulk=False)
    #
    #         # 若存在，修改style_id 或language_id
    #         else:
    #             # get_style_id = MusicStyle.objects.filter(style__contains=tag).values('id')
    #
    #             # 如果查询的此tag不在MusicStyle表中,就去MusicLanguage中查找，若都没有，放弃此标签
    #             if len(get_style_id) == 0:  # 若此tag不在MusicStyle中
    #                 # 在MusicLanguage中查找
    #                 # get_language_id = MusicLanguage.objects.filter(language__contains=tag).values('id')
    #                 # 若不在，放弃此标签
    #                 if len(get_language_id) == 0:
    #                     print("数据库中不存在此标签")
    #                 else:
    #                     # 获取在MusicLanguage中查询到的对应tag的id
    #                     language_id = get_language_id[0].get('id')
    #                     # 修改SongList中language_id
    #                     SongList.objects.filter(list_id__exact=list_id).update(language_id=language_id)
    #
    #             else:
    #                 # 若在MusicStyle中有此tag，那么更新style_id的值
    #                 style_id = get_style_id[0].get('id')   # 获取MusicStyle对应tag的id
    #                 SongList.objects.filter(list_id__exact=list_id).update(style_id=style_id)


    # 歌单中的歌曲[{},{}]

    print("结束。。。")

    return render(request, "index.html")
    # return HttpResponse("ojbk")