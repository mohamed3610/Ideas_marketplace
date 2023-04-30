from django.shortcuts import render , redirect , reverse
from .models import Tags , Files , Features , Ideas , Projects
from django.contrib import messages

# Create your views here.

def submit_Idea(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["name"]
            description = request.POST["description"]
            problem_to_solve = request.POST["problem_to_solve"]
            if Ideas.objects.filter(name = name).exists():
                messages.error(request, f"An Idea with the name '{name}' already exists. Please review the existing idea to see if you can add your input or choose a different name for your new idea.", extra_tags='error')
            
            else:
                idea_id = Ideas.objects.create(name = name , description = description , problem_to_solve = problem_to_solve , employee = request.user)
                return redirect(reverse("submit_files" ,args=[idea_id.id]))
            
        else:
            return render(request , "Ideas/add_ideas.html")
        
    else:
        return redirect("register")
    
def add_files(request , idea_id):
    idea = Ideas.objects.get(id = idea_id)
    return render(request,"Ideas/add_files.html" , {
        "idea":idea
    }) 