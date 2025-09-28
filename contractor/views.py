import os
from django.conf import settings
from django.shortcuts import render
from The_Builder.models import Users
from The_Builder.settings import BASE_DIR
from datetime import datetime

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
# Create your views here.
def contractor_home(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    return render(request, 'contractor_home.html',{"obj":obj})

def contractore_view_profile(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    return render(request, 'contractor_view_profile.html',{"obj":obj})

def contractore_edit_profile(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    if request.method=="POST":
        # You can access individual fields like this:
        try:
            user_fullname = request.POST.get("fullname")
            user_address = request.POST.get("address")  
            user_profile_image = request.FILES.get("profile_picture")  # For file uploads
            user_profile =request.POST.get("profile")
            user_city = request.POST.get("city")
            user_state = request.POST.get("state")
            user_zip_code = request.POST.get("zip_code")
            user_country = request.POST.get("country")
            user_about_me = request.POST.get("about_me")
            print(user_fullname, user_address, user_city, user_profile_image, user_state, user_zip_code, user_country, user_about_me)
            print("Profile id:", token_data["user_id"])
            ext=user_profile_image.name.split('.')[-1]


            if user_profile_image:
                upload_folder = os.path.join(settings.MEDIA_ROOT,"profile_images")
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                ext=user_profile_image.name.split('.')[-1]
                file_name=f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{obj.user_id}.{ext}"
                file_path=os.path.join(upload_folder,file_name)
                with open(file_path,"wb+") as f:
                    for chunk in user_profile_image.chunks():
                        f.write(chunk)
                

            Users.objects.filter(user_id=token_data["user_id"]).update(
                user_full_name=user_fullname,
                user_address=user_address,
                user_city=user_city,
                user_profile=user_profile,
                user_profile_pic=file_name,
                user_state=user_state,
                user_zipcode=user_zip_code,
                user_country=user_country,
                user_about=user_about_me
            )
            return render(request,'contractor_view_profile.html')
        except Exception as e:
            print("Error updating profile:", e)
        # Here, you would typically save the updated profile information to the database.
    
    return render(request, 'contractor_edit_profile.html',{"obj":obj})