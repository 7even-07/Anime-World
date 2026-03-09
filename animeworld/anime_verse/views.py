from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import HeroSectionSlider, Anime, AnimeWorld, BlogFilter, Category, HomePageSideBanner, HomePageVideo, UpcommingEvent, SubscribeComic, UserProfile
from django.contrib import messages
from .forms import UserForm, UserProfileForm, AnimeWorldForm
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
import io
import uuid
from django.core.paginator import Paginator

def index(request):
    # hero section slider details
    hero_section_slider_details = HeroSectionSlider.objects.filter(is_active=True, is_delete=False)

    # anime world details
    comics_list = AnimeWorld.objects.filter(is_active=True, is_delete=False).order_by('-created_at')
    paginator = Paginator(comics_list, 16)
    page_number = request.GET.get('page')
    anime_world_details = paginator.get_page(page_number)


    # blog filters
    blog_filters = BlogFilter.objects.filter(is_active=True, is_delete=False)

    # Global latest
    latest_global = AnimeWorld.objects.filter(
            is_active=True,
            is_delete=False
        ).select_related('anime_name').order_by('-created_at')
    
    # trending blogs
    trending_blogs = AnimeWorld.objects.filter(
        is_trending=True,
        is_active=True,
        is_delete=False
    ).order_by("-created_at")[:4]

    # categories
    categories = Category.objects.filter(is_active=True, is_delete=False).order_by('-created_at')

    # homepage side banner
    homepage_side_banner = HomePageSideBanner.objects.filter(is_active=True, is_delete=False).first()

    # homepage video
    homepage_video = HomePageVideo.objects.filter(is_active=True, is_delete=False).first()

    # upcomming event
    upcomming_event = UpcommingEvent.objects.filter(is_active=True, is_delete=False).first()

    # subscribe comics
    if request.method == "POST" and request.POST.get("form_type") == "subscribe_comics":
        email_addr = request.POST.get("email_addr", "").strip()

        if email_addr:
            SubscribeComic.objects.create(
                email_addr=email_addr
            )
            messages.success(request, "Your message has been successfully sent to us.")
        else:
            messages.error(request, "All fields are required.")
            return redirect("index")
        
    context = {
        "hero_section_slider_details": hero_section_slider_details, 
        "anime_world_details": anime_world_details, 
        "blog_filters": blog_filters, 
        "latest_global": latest_global,
        "trending_blogs": trending_blogs,
        "categories": categories,
        "homepage_side_banner": homepage_side_banner,
        "homepage_video": homepage_video,
        "upcomming_event": upcomming_event
        }
    
    return render(request, "index.html", context)

def category_details(request, id):
    comics = AnimeWorld.objects.filter(category__id=id, is_active=True, is_delete=False).prefetch_related('category', 'anime_name', 'user').order_by('-created_at')
    recent_comic = comics.first()

    if recent_comic:
        comics = comics.exclude(id=recent_comic.id)
    context = {
        "comics": comics,
        "recent_comic": recent_comic,

    }
    return render(request, "category_details.html", context)

def about_page(request):
    return render(request, "about.html")

def contact_page(request):
    return render(request, "contact.html")

# comic details page
def comic_detail(request, id):
    comic = AnimeWorld.objects.get(id=id, is_active=True, is_delete=False)
    related_comics = AnimeWorld.objects.filter(anime_name=comic.anime_name).exclude(id=id)[:4]
    context = {
        "comic": comic,
        "related_comics": related_comics
    }
    return render(request, "comic_detail.html", context)

def read_first(request, id):
    comic = AnimeWorld.objects.get(id=id, is_active=True, is_delete=False)
    context = {"comic": comic,
               "start_page": 1         
    }
    return render(request, "pdf_reader.html", context)

def read_last(request, id):
    comic = AnimeWorld.objects.get(id=id, is_active=True, is_delete=False)
    # calculate the last page
    from PyPDF2 import PdfReader
    pdf_path = comic.comics.path
    pdf_file = open(pdf_path, "rb")
    reader = PdfReader(pdf_file)
    last_page = len(reader.pages)
    pdf_file.close()

    context = {"comic": comic,
               "start_page": last_page         
    }
    return render(request, "pdf_reader.html", context)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # update profile (signal already created it)
        profile = user.userprofile
        profile.full_name = request.POST["full_name"]
        profile.phone = request.POST["phone"]
        profile.gender = request.POST.get("gender")
        profile.save()

        # auto login
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)

        messages.success(request, "Account successfully created!")
        return redirect("index")

    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("login")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successfull.")
            return redirect("index")
        else:
            messages.error(request, "Invalid password.")
            return redirect("login")

    return render(request, "login.html")

def logout_user(request):
    if request.method == "POST":
        auth_logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect("login")


@login_required
def profile_view(request):
    # user details handling
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please fix the error below.")
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=request.user.userprofile)


    comics_list = request.user.comics.filter(is_active=True, is_delete=False).order_by('-created_at')

    paginator = Paginator(comics_list, 8)
    page_number = request.GET.get('page')
    active_tab = request.GET.get("tab", "general") # default tab
    user_comics = paginator.get_page(page_number)

    context = {
        "user_form": user_form,
        "user_profile_form": user_profile_form,
        "user_comics": user_comics,
        "active_tab": active_tab
    }
    return render(request, "user_profile.html", context)


@login_required
def add_comic(request):

    animes = Anime.objects.filter(is_active=True, is_delete=False)
    categories = Category.objects.filter(is_active=True, is_delete=False)

    comic_form = AnimeWorldForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST":

        if comic_form.is_valid():

            comic = comic_form.save(commit=False)
            comic.user = request.user

            pdf_file = request.FILES.get("comic_pdf_file")
            image_files = request.FILES.getlist("comic_images")

            if pdf_file and image_files:
                messages.error(request, "Upload either PDF or Images, not both.")

            elif image_files:
                images = []

                for image in image_files:
                    img = Image.open(image)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    images.append(img)

                pdf_io = io.BytesIO()
                images[0].save(
                    pdf_io,
                    format="PDF",
                    save_all=True,
                    append_images=images[1:]
                )

                pdf_name = f"{uuid.uuid4()}.pdf"
                comic.comics.save(pdf_name, ContentFile(pdf_io.getvalue()), save=False)

                comic.save()
                comic_form.save_m2m()
                messages.success(request, "Comic uploaded successfully.")
                return redirect("add_comic")

            elif pdf_file:
                comic.comics = pdf_file
                comic.save()
                comic_form.save_m2m()
                messages.success(request, "Comic uploaded successfully.")
                return redirect("add_comic")

            else:
                messages.error(request, "Upload PDF or Images")

        else:
            for field, errors in comic_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    context = {
        "comic_form": comic_form,
        "animes": animes,
        "categories": categories
    }

    return render(request, "add_comic.html", context)

@login_required
def edit_comic(request, id):
    comic = get_object_or_404(AnimeWorld, id=id, user=request.user)

    anime = Anime.objects.filter(is_active=True, is_delete=False)
    categories = Category.objects.filter(is_active=True, is_delete=False)
    comic_form = AnimeWorldForm(
        request.POST or None,
        request.FILES or None,
        instance=comic
    )

    if request.method == "POST":
        if comic_form.is_valid():

            comic = comic_form.save(commit=False)

            pdf_file = request.FILES.get("comic_pdf_file")
            image_files = request.FILES.getlist("comic_images")

            if pdf_file and image_files:
                messages.error(request, "Upload either PDF or Images, not both.")
            
            elif image_files:
                images = []

                for image in image_files:
                    img = Image.open(image)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    images.append(img)

                pdf_io = io.BytesIO()
                images[0].save(
                    pdf_io,
                    format="PDF",
                    save_all=True,
                    append_images=images[1:]
                )

                pdf_name = f"{uuid.uuid4()}.pdf"
                comic.comics.save(pdf_name, ContentFile(pdf_io.getvalue()), save=False)

            elif pdf_file:
                comic.comics = pdf_file

            comic.save()
            messages.success(request, "Comic updated successfully")
            return redirect("profile")
        
        else:
            for field, errors in comic_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    context = {
        "comic_form": comic_form,
        "animes": anime,
        "categories": categories,
        "comic": comic
    }

    return render(request, "edit_comic.html", context)

@login_required
def delete_comic(request, id):
    comic = get_object_or_404(AnimeWorld, id=id, user=request.user)

    if request.method == "POST":
        comic.is_active = False
        comic.is_delete = True
        comic.save()
        messages.success(request, "Comic has been deleted successfully.")
        return redirect("profile")
    return redirect("profile")