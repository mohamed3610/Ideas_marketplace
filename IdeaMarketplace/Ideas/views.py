from django.shortcuts import render , redirect , reverse
from .models import Tags , Files , Features , Ideas , Projects
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def submit_Idea(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["name"]
            description = request.POST["description"]
            problem_to_solve = request.POST["problem_to_solve"]
            if Ideas.objects.filter(name = name).exists():
                messages.error(request, f"An Idea with the name '{name}' already exists. Please review the existing idea to see if you can add your input or choose a different name for your new idea.", extra_tags='error')
                return render(request , "Ideas/add_ideas.html")
            else:
                idea_id = Ideas.objects.create(name = name , description = description , problem_to_solve = problem_to_solve , employee = request.user)
                return redirect(reverse("submit_files" ,args=[idea_id.id]))
            
        else:
            return render(request , "Ideas/add_ideas.html")
        
    else:
        return redirect("register")
    
def add_files(request , idea_id):
    idea = Ideas.objects.get(id = idea_id)
    if request.method == "POST":
        files = request.FILES.getlist('files')
        for file in files:
            single_file = Files.objects.create(file = file , employee = request.user)
            idea.files.add(single_file)
        return redirect(reverse("add_tags", args=[idea.id]))
    


    return render(request,"Ideas/add_files.html" , {
        "idea_id":idea,
    }) 

def add_tags(request, idea_id):
    idea = Ideas.objects.get(id=idea_id)

    if request.method == 'POST':
        tag_name = request.POST['tags']
        if Tags.objects.filter(tag=tag_name).exists():
            idea.tags.add(Tags.objects.filter(tag=tag_name)[0])
        else:
            tag = Tags.objects.create(tag=tag_name)
            idea.tags.add(tag)

        if 'add_tag' in request.POST:
            # Add tag button was clicked, redirect back to the same page
            return redirect(reverse('add_tags', args=[idea_id]))
        elif 'finish' in request.POST:
            # Finish button was clicked, redirect to another page
            return redirect(reverse('view_idea', args = [idea_id]))

    return render(request, 'Ideas/add_tags.html', {
        'idea_id': idea_id,
    })


def view_idea(request,idea_id):
    if request.user.is_authenticated:
        idea = Ideas.objects.get(pk=idea_id)
        return render(request , "Ideas/view_idea.html", {
            "idea_id" : idea_id,
            "idea":idea,
        })

@user_passes_test(lambda u: u.groups.filter(name__in=['HR', 'Marketing']).exists())
def add_score(request):
    pass