from django.db import models
from django.contrib.auth.models import User

class DefaultProfile(models.Model):
    title = models.CharField(max_length=255)
    img_src = models.ImageField(upload_to="default_profiles")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Prefer not to say"),
    ]

    COUNTRY_CHOICES = [
        ("India", "India"),
        ("Japan", "Japan"),
        ("USA", "USA"),
        ("Canada", "Canada"),
        ("UK", "UK"),
        ("Germany", "Germany"),
        ("France", "France"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    img_src = models.ImageField(upload_to="users/profiles", blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, default="")
    bio = models.TextField(blank=True, default="")
    country = models.CharField(max_length=100, blank=True, default="", choices=COUNTRY_CHOICES)
    website = models.URLField(max_length=255, blank=True, default="")
    twitter = models.URLField(max_length=255, blank=True, default="")
    facebook = models.URLField(max_length=255, blank=True, default="")
    google = models.URLField(max_length=255, blank=True, default="")
    linkdin = models.URLField(max_length=255, blank=True, default="")
    instagram = models.URLField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class HeroSectionSlider(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    link = models.CharField(max_length=255)
    img_src = models.ImageField(upload_to="hero_section_slider")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "hero_section_slider"

class Anime(models.Model):
    anime_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)


    def __str__(self):
        return self.anime_name

    class Meta:
        db_table = "anime"

class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "category"

class AnimeWorld(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comics")
    anime_name = models.ForeignKey(Anime, related_name="anime_world", on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="posts", blank=True)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    link = models.URLField(max_length=255, null=True, blank=True)
    img_src = models.ImageField(upload_to="anime/covers")
    comics = models.FileField(upload_to="anime/comics", null=True)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "anime_world"
    
class BlogFilter(models.Model):
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "blog_filter"

class HomePageSideBanner(models.Model):
    title = models.CharField(max_length=255)
    img_src = models.ImageField(upload_to="banners/sidebar")
    link = models.URLField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "homepage_side_banner"

class HomePageVideo(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    img_src = models.ImageField(upload_to="banners/videos")
    link = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "homepage_video"


class UpcommingEvent(models.Model):
    anime_name = models.ForeignKey(Anime, related_name="upcomming_event", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    img_src = models.ImageField(upload_to="banners/upcomming-events")
    link = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "upcomming_event"

class SubscribeComic(models.Model):
    email_addr = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.email_addr
    
    class Meta:
        db_table = "subscribe_comic"


