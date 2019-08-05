from django.db import models

# Create your models here.


class Music(models.Model):
    music_id = models.CharField(max_length=255, null=False)
    music_name = models.CharField(max_length=255, null=False)
    # music_url = models.CharField(max_length=255, null=True, default="")
    music_img = models.CharField(max_length=255, null=False)
    music_author = models.CharField(max_length=255, null=False)
    music_album = models.CharField(max_length=255, null=False)
    # music_list_id = models.CharField(max_length=255, null=False)
    music_list_id = models.ForeignKey('SongList', on_delete=models.DO_NOTHING)


class MusicLanguage(models.Model):
    language = models.CharField(max_length=200)


class MusicStyle(models.Model):
    style = models.CharField(max_length=200)


class SongList(models.Model):
    list_id = models.CharField(max_length=100)
    list_title = models.CharField(max_length=500)
    list_img = models.CharField(max_length=500)
    list_tag = models.CharField(max_length=500)
    language = models.ForeignKey(MusicLanguage, models.DO_NOTHING)
    style = models.ForeignKey(MusicStyle, models.DO_NOTHING)


class MV(models.Model):
    mv_id = models.CharField(max_length=100)
    mv_name = models.CharField(max_length=500)
    mv_author = models.CharField(max_length=100)
    mv_desc = models.CharField(max_length=800)
    mv_pic = models.CharField(max_length=500)
    playCount = models.CharField(max_length=100)
    publishTime = models.CharField(max_length=100)
    mv_url_240 = models.CharField(max_length=800, null=True, default="")
    mv_url_480 = models.CharField(max_length=800, null=True, default="")
    mv_url_720 = models.CharField(max_length=800, null=True, default="")
    mv_url_1080 = models.CharField(max_length=800, null=True, default="")

    # def __str__(self):
    #     return '{"mv_id":"{}","mv_name":"{}""mv_author":"{}","mv_desc":"{}","mv_pic":"{}","playCount":"{}","publishTime":"{}","mv_url_240":"{}","mv_url_480":"{}","mv_url_720":"{}","mv_url_1080":"{}"}'.format(self.mv_id,self.mv_name,self.mv_author,self.mv_desc,self.mv_pic,self.playCount,self.publishTime,self.mv_url_240,self.mv_url_480,self.mv_url_720,self.mv_url_1080)


class User(models.Model):
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=500, null=False)
    email = models.CharField(max_length=100, null=False, default="")


class Admin(models.Model):
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=255, null=False)
