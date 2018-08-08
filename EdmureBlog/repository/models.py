from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像')

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'))

    def __str__(self):
        return self.username

class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64,null=True,blank=True)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid',on_delete=None)



class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users',on_delete=None)
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers',on_delete=None)

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=None)
    # blog_id = 1

# blog = Blog.objects.filter(site='bingdujieer').first()
# info = obj.user
# category_list = Category.objects.filter(blog_id=blog.nid)

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容', )

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid',on_delete=None)


class UpDown(models.Model):
    """
    点赞表
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid',on_delete=None)
    user = models.ForeignKey(verbose_name='点赞用户', to='UserInfo', to_field='nid',on_delete=None)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True,on_delete=None)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid',on_delete=None)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid',on_delete=None)

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=None)
    # m = xx
# blog = Blog.objects.filter(site='bingdujieer').first()
# info = obj.user
# category_list = Category.objects.filter(blog_id=blog.nid)
# Tag.objects.filter(blog_id=blog.nid)

class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid',on_delete=None)
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', blank=True, null=True,on_delete=None)

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "OpenStack"),
        (4, "GoLang"),
    ]
    # 1,2,3,4
    article_type_id = models.IntegerField(choices=type_choices, default=None)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )


class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid',on_delete=None)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid',on_delete=None,blank=True, null=True)

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

# http://127.0.0.1:8000/wupeiqi/tag/1.html

# 自定义第三张表
# a2t = Article2Tag.objects.filter(tag_id=1,blog_id=blog.nid)
# for item in a2t:
#     item.article.title...

# 自动生成第三张表
# Article.objects.filter(m=1,blog_id=blog.nid)
# Article.objects.filter(tag_set=1,blog_id=blog.nid)


# 自定义第三张表+M2M
# Article.objects.filter(tags=1,blog_id=blog.nid)


class Tpl(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()


class Trouble(models.Model):
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey(UserInfo,related_name='u',on_delete=None)
    # ctime = models.CharField(max_length=32) # 1491527007.452494
    ctime = models.DateTimeField()
    status_choices = (
        (1,'未处理'),
        (2,'处理中'),
        (3,'已处理'),
    )
    status = models.IntegerField(choices=status_choices,default=1)

    processer = models.ForeignKey(UserInfo,related_name='p',null=True,blank=True,on_delete=None)
    solution = models.TextField(null=True)
    ptime = models.DateTimeField(null=True)
    pj_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '活很好'),
    )
    pj = models.IntegerField(choices=pj_choices,null=True,default=2)
















