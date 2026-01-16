import os
from django.conf import settings
from django.shortcuts import redirect, render
from The_Builder.models import Users
from The_Builder.settings import BASE_DIR
from datetime import datetime, date
from django.contrib import messages

from thekedar.models import ProjectApplication


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
# Create your views here.
def thekedar_home(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    return render(request, 'thekedar_home.html', {'obj': obj})

def thekedar_profile(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    return render(request, 'thekedar_profile.html', {'obj': obj})


def thekedar_profile_edit(request):
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
            return redirect('/thekedar/profile/')
        except Exception as e:
            print("Error updating profile:", e)
            return render(request, 'thekedar_profile_edit.html',{"obj":obj})
    return render(request, 'thekedar_profile_edit.html', {'obj': obj})

from contractor.models import ContractorProject
def thekedar_projects_all(request):
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    print("Thekedar:", obj)
    projects = ContractorProject.objects.select_related('user').prefetch_related("files").all()
    print("Projects:", projects)
    return render(request, 'projects_all.html', {'obj': obj, 'projects': projects})



def apply_project(request):
    project_id = request.GET.get("id")
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])
    projects = ContractorProject.objects.select_related('user').filter(id=project_id).first()
    if ProjectApplication.objects.filter(
        project=projects,
        applicant=obj
    ).exists():
        messages.warning(request, "You have already applied for this project.")
        return redirect(f"/thekedar/project_details?id={projects.id}")

    if request.method=="POST":
        experience_years = request.POST.get("experience_years")
        proposed_budget = request.POST.get("proposed_budget")
        estimated_duration = request.POST.get("estimated_duration")
        machines_equipment = request.POST.get("machines_equipment")
        why_select_you = request.POST.get("why_select_you")

        # Basic validation
        if not all([
            experience_years,
            proposed_budget,
            estimated_duration,
            machines_equipment,
            why_select_you
        ]):
            messages.error(request, "All fields are required.")
            return render(
                request,
                "apply_project.html",
                {"project": projects, "obj": obj}
            )

        # Save application
        ProjectApplication.objects.create(
            project=projects,
            applicant=obj,
            experience_years=experience_years,
            proposed_budget=proposed_budget,
            estimated_duration=estimated_duration,
            machines_equipment=machines_equipment,
            why_select_you=why_select_you,
        )

        messages.success(request, "Application submitted successfully.")
        return redirect(f"/thekedar/project_details?id={projects.id}")
    else:

        print(projects)
        return render(request, "apply_project.html",{'obj': obj, 'project': projects})




from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Max
from contractor.models import Message

def project_details(request):
    project_id = request.GET.get("id")

    if not project_id:
        return redirect("/thekedar/projects_all/")

    # Logged-in user
    token_data = request.session.get("data")
    obj = Users.objects.get(user_id=token_data["user_id"])

    # Project with attachments
    project = get_object_or_404(
        ContractorProject.objects
        .select_related("user")
        .prefetch_related("files"),
        id=project_id
    )

    return render(
        request,
        "project_details.html",
        {
            "obj": obj,
            "project": project
        }
    )


def messages_list(request):
    """List all conversations for the logged-in thekedar"""
    token_data = request.session.get("data")
    if not token_data:
        return redirect("/")
    
    obj = Users.objects.get(user_id=token_data["user_id"])
    
    # Get all unique users the thekedar has messaged with
    sent_messages = Message.objects.filter(sender=obj).values('receiver').annotate(
        latest_message_time=Max('created_at')
    )
    received_messages = Message.objects.filter(receiver=obj).values('sender').annotate(
        latest_message_time=Max('created_at')
    )
    
    # Combine and get unique users
    conversations = {}
    
    # Process sent messages
    for msg in sent_messages:
        receiver_id = msg['receiver']
        if receiver_id not in conversations or msg['latest_message_time'] > conversations[receiver_id]['latest_time']:
            latest_msg = Message.objects.filter(
                Q(sender=obj, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver=obj)
            ).order_by('-created_at').first()
            conversations[receiver_id] = {
                'user_id': receiver_id,
                'latest_time': msg['latest_message_time'],
                'latest_message': latest_msg
            }
    
    # Process received messages
    for msg in received_messages:
        sender_id = msg['sender']
        if sender_id not in conversations or msg['latest_message_time'] > conversations[sender_id]['latest_time']:
            latest_msg = Message.objects.filter(
                Q(sender=obj, receiver_id=sender_id) | Q(sender_id=sender_id, receiver=obj)
            ).order_by('-created_at').first()
            conversations[sender_id] = {
                'user_id': sender_id,
                'latest_time': msg['latest_message_time'],
                'latest_message': latest_msg
            }
    
    # Get user details and unread counts
    conversation_list = []
    for user_id, conv_data in conversations.items():
        try:
            other_user = Users.objects.get(user_id=user_id)
            unread_count = Message.objects.filter(
                sender=other_user,
                receiver=obj,
                is_read=False
            ).count()
            
            conversation_list.append({
                'user': other_user,
                'latest_message': conv_data['latest_message'],
                'unread_count': unread_count,
                'latest_time': conv_data['latest_time']
            })
        except Users.DoesNotExist:
            continue
    
    # Sort by latest message time
    conversation_list.sort(key=lambda x: x['latest_time'], reverse=True)
    
    return render(
        request,
        'messages_list_thekedar.html',
        {
            'obj': obj,
            'conversations': conversation_list
        }
    )


def conversation_view(request, user_id):
    """View conversation with a specific user"""
    token_data = request.session.get("data")
    if not token_data:
        return redirect("/")
    
    obj = Users.objects.get(user_id=token_data["user_id"])
    other_user = get_object_or_404(Users, user_id=user_id)
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=obj, is_read=False).update(is_read=True)
    
    # Get all messages between these two users
    messages = Message.objects.filter(
        Q(sender=obj, receiver=other_user) | Q(sender=other_user, receiver=obj)
    ).order_by('created_at')
    
    # Handle POST request (sending new message)
    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            Message.objects.create(
                sender=obj,
                receiver=other_user,
                message=message_text
            )
            return redirect(f'/thekedar/messages/{user_id}/')
    
    return render(
        request,
        'conversation_thekedar.html',
        {
            'obj': obj,
            'other_user': other_user,
            'messages': messages
        }
    )