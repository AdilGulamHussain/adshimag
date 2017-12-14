from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models import permalink
from django.template.defaultfilters import slugify


class MagUser(models.Model):
    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    phone_regex = RegexValidator(regex=r'^0\d{10}$', message="Phone number must be entered. 11 Digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    password = models.CharField(max_length=64, null=True)
    logged_in = models.BooleanField(default=False)

    def get_full_name(self):
        """
        Gets the full name of the user object.
        :return: first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Gets the shorten variant of the name of the user object.
        :return: Short name for the user.
        """
        return self.first_name

    def is_authenticated(self):
        return self.email != "anon@default.com" and self.logged_in


class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'view_category', None, {'slug': self.slug}

    def save(self, *args, **kwargs):
        """
        Auto create the slug before saving a new Category.
        """
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    date_posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.ManyToManyField(MagUser)
    # img_url = models.CharField(max_length=250, null=True, default=None)

    @permalink
    def get_absolute_url(self):
        return 'view_article', None, {'slug': self.slug}

    class Meta:
        get_latest_by = "date_posted"

    def add_like(self, user):
        self.likes.add(user)

    def remove_like(self, user):
        self.likes.remove(user)

    def save(self, *args, **kwargs):
        """
        Auto create the slug before saving a new Article.
        """
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(MagUser, on_delete=models.CASCADE)
    body = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    date_time = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user.get_short_name(), self.article.title)
