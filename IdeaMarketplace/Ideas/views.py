from django.shortcuts import render , redirect , reverse
from .models import Tags , Files , Features , Ideas , Projects
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import os
import io
import zipfile
from django.http import HttpResponse
import asyncio
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import ScoreForm

# Create your views here.


def view_Ideas(request):
    if request.user.is_authenticated:
        ideas = Ideas.objects.filter().all()
        return render(request , "Ideas/view_all_ideas.html" , {"ideas":ideas})
    else:
        return HttpResponse("Unauthorized", status=401)


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
            tag, created = Tags.objects.get_or_create(tag=tag_name)
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





def download_idea_files_as_zip(idea):
    # Check if the idea has files
    if not idea.files.exists():
        return None

    # Create a ZIP file containing all files associated with the idea
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, False) as zip_file:
            for file in idea.files.all():
                try:
                    file_content = file.file.read()
                    zip_file.writestr(file.file.name, file_content)
                except Exception as e:
                    # Handle file reading errors
                    # Log the error or take appropriate action
                    pass

        return ContentFile(zip_buffer.getvalue())

def download_idea_files(request, idea_id):
    idea = get_object_or_404(Ideas, id=idea_id)

    zip_filename = f"{idea.name}_files.zip"
    zip_file_content = download_idea_files_as_zip(idea)

    if zip_file_content:
        try:
            default_storage.save(zip_filename, zip_file_content)

            response = HttpResponse(content_type="application/zip")
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            response.write(default_storage.open(zip_filename, 'rb').read())

            # Delete the temporary ZIP file
            default_storage.delete(zip_filename)

            return response
        except Exception as e:
            # Handle file saving errors
            # Log the error or take appropriate action
            return HttpResponseBadRequest("Error creating ZIP file")

    return HttpResponseBadRequest("No files to download")

def view_idea(request, idea_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    idea = get_object_or_404(Ideas, id=idea_id)

    return render(request, 'Ideas/view_idea.html', {'idea': idea, 'idea_id': idea_id})



# @user_passes_test(lambda u: u.groups.filter(name__in=['HR', 'Marketing']).exists())
def add_score(request, idea_id):
    idea = Ideas.objects.get(pk=idea_id)
    
    if request.method == 'POST':
        form = ScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.creator = request.user
            score.idea = idea
            score.save()
            
            return redirect('view_all_ideas')  # Redirect to a success page or another view
    else:
        form = ScoreForm()

    return render(request, 'Ideas/add_score.html', {'form': form, 'idea': idea})









@sync_to_async
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

@sync_to_async
def create_zipfile(zip_filepath, tmp_dir):
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tmp_dir):
            for file in files:
                zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), tmp_dir))

async def download_files(request, idea_id):
    idea = get_object_or_404(Ideas, id=idea_id)

    tmp_dir = "/tmp/myfiles"
    await create_directory(tmp_dir)

    files = idea.files.all()

    for file in files:
        file_path = file.file.path
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            data = f.read()
        with open(os.path.join(tmp_dir, filename), 'wb') as f:
            f.write(data)

    zip_filename = 'idea_files.zip'
    zip_filepath = os.path.join(tmp_dir, zip_filename)
    await create_zipfile(zip_filepath, tmp_dir)

    with open(zip_filepath, 'rb') as f:
        data = f.read()
    response = HttpResponse(data, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    os.remove(zip_filepath)
    os.rmdir(tmp_dir)

    return response