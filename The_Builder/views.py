from django.shortcuts import render, redirect
import requests

def home(request):
    return render(request, 'base.html')


def register(request):
    if request.method=="POST":
            user_fullname=request.POST.get("fullname")
            user_username=request.POST.get("username")
            user_email=request.POST.get("email")
            user_phone=request.POST.get("phone")
            user_password=request.POST.get("password")
            user_type=request.POST.get("role")
            user_is_active=True
            print(user_fullname,user_username,user_email,user_phone,user_password,user_type,user_is_active)
            url = f"http://{request.get_host()}/api/register/"
            payload = {
                "user_full_name": user_fullname,
                "user_username": user_username,
                "user_email": user_email,
                "user_phone": user_phone,
                "user_password": user_password,
                "user_type": user_type,
                "user_is_active": user_is_active
            }
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)

            # Response check
            if response.status_code == 201:
                print("✅ Success:", response.json())
                return render(request, 'register.html', {"message": "User registered successfully!"})
            else:
                print("❌ Error:", response.status_code, response.text)
                return render(request, 'register.html', {"error": "Registration failed. Please try again."})
    return render(request, 'register.html')

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email,password)
        url = f"http://{request.get_host()}/api/login/"
        payload = {"user_email": email, "user_password": password}
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"})

        try:
            data = r.json()
            print("Response JSON:", data)  # Debugging
            if data.get("status"):
                user_type = data["data"]["user_type"]
                print(user_type)
                if user_type == "contractor":
                    print("Redirect to Contractor Dashboard")
                    request.session["data"] = data["data"]
                    return redirect('/contractor/')
                elif user_type == "thekedar":
                    print("Redirect to Thekedar Dashboard")
                    request.session["data"] = data["data"]
                    return redirect('/thekedar/')
                elif user_type == "worker":
                    print("Redirect to Worker Dashboard")
                    request.session["data"] = data["data"]
                    return redirect('/worker/')
                else:
                    print("Redirect to Default Dashboard")
            else:
                print("❌ Login failed:", data.get("message"))

        except ValueError:
            print("Non-JSON response (status_code={}):".format(r.status_code))
            print(r.text[:1000])  # Debugging
    return render(request, 'login.html')