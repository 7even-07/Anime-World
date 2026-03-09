from django.contrib import admin
from .models import HeroSectionSlider, Anime, AnimeWorld, BlogFilter, Category, HomePageSideBanner, HomePageVideo, UpcommingEvent, UserProfile,DefaultProfile


@admin.register(HeroSectionSlider)
class HeroSectionSliderAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "img_src", "created_at","is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("anime_name","is_active", "is_delete",)
    search_fields = ("anime_name", "created_at",)
    list_filter = ("created_at",)

@admin.register(AnimeWorld)
class AnimeWorldAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "img_src", "created_at","is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)

@admin.register(BlogFilter)
class BlogFilterAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)

@admin.register(HomePageSideBanner)
class HomePageSideBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "created_at", "is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)

@admin.register(HomePageVideo)
class HomePageVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "created_at", "is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)

@admin.register(UpcommingEvent)
class UpcommingEventAdmin(admin.ModelAdmin):
    list_display = ("title", "link", "created_at", "is_active", "is_delete",)
    search_fields = ("title", "created_at",)
    list_filter = ("created_at",)


admin.site.register(DefaultProfile)

admin.site.register(UserProfile)

