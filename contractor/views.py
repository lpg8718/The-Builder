import os
from django.conf import settings
from django.shortcuts import redirect, render
from The_Builder.models import Users
from The_Builder.settings import BASE_DIR
from datetime import datetime, date
from django.contrib import messages

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
            user_fullname = request.POST.get("fullname","")
            user_address = request.POST.get("address","")  
            user_profile_image = request.FILES.get("profile_picture","")  # For file uploads
            user_profile =request.POST.get("profile","")
            user_city = request.POST.get("city","")
            user_state = request.POST.get("state","")
            user_zip_code = request.POST.get("zip_code","")
            user_country = request.POST.get("country","")
            user_about_me = request.POST.get("about_me","")
            print(user_fullname, user_address, user_city, user_profile_image,user_profile, user_state, user_zip_code, user_country, user_about_me)
            print("Profile id:", token_data["user_id"])


            if user_profile_image:
                ext=user_profile_image.name.split('.')[-1]
                print("Uploading new profile image")
                upload_folder = os.path.join(settings.MEDIA_ROOT,"profile_images")
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                ext=user_profile_image.name.split('.')[-1]
                file_name=f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{obj.user_id}.{ext}"
                file_path=os.path.join(upload_folder,file_name)
                with open(file_path,"wb+") as f:
                    for chunk in user_profile_image.chunks():
                        f.write(chunk)
            else:
                print("No new profile image uploaded")
                file_name= obj.user_profile_pic
                
                

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
            return redirect('/contractor/profile/')
        except Exception as e:
            print("Error updating profile:", e)
            return render(request, 'contractor_edit_profile.html',{"obj":obj})
        # Here, you would typically save the updated profile information to the database.
    
    return render(request, 'contractor_edit_profile.html',{"obj":obj})

def project_page1(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])

    # ✔ Get all projects of this user
    from contractor.models import ContractorProject
    user_projects = ContractorProject.objects.filter(user=obj)

    return render(request, 'project_page1.html', {
        "obj": obj,
        "projects": user_projects,
        "today": date.today()
    })


def add_project(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])

    if request.method == "POST":
        project_title = request.POST.get("project_title")
        project_category = request.POST.get("project_category")
        budget = request.POST.get("budget")
        payment_terms = request.POST.get("payment_terms")
        advance_payment = request.POST.get("advance_payment")
        state = request.POST.get("state")
        city = request.POST.get("city")
        full_address = request.POST.get("full_address")
        start_date = request.POST.get("start_date")
        deadline = request.POST.get("deadline")
        required_workers = request.POST.get("workers")
        required_skills = request.POST.get("skills")
        project_description = request.POST.get("project_description")

        # ⛔ WRONG: request.FILES.get("attachments")
        # ✅ Correct: getlist()
        files = request.FILES.getlist("attachments")

        # -----------------------------------------------------
        # 1) Create Project
        # -----------------------------------------------------
        from contractor.models import ContractorProject, ProjectAttachment

        new_project = ContractorProject.objects.create(
            user=obj,
            project_title=project_title,
            project_category=project_category,
            budget=budget,
            payment_terms=payment_terms,
            advance_payment=advance_payment,
            state=state,
            city=city,
            full_address=full_address,
            start_date=start_date,
            deadline=deadline,
            required_workers=required_workers,
            required_skills=required_skills,
            project_description=project_description,
        )

        # -----------------------------------------------------
        # 2) Save Multiple Attachments
        # -----------------------------------------------------
        for f in files:
            ProjectAttachment.objects.create(
                project=new_project,
                file=f
            )
        messages.success(request, "🎉 Project added successfully!")
        return redirect('/contractor/project_page1/')

    return render(request, 'add_projects.html',{"obj":obj})


from django.shortcuts import render, get_object_or_404, redirect
from contractor.models import ContractorProject
def view_project(request,project_id):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    project = get_object_or_404(ContractorProject, id=project_id)
    return render(request, 'view_project.html',{"obj":obj,"project":project})

