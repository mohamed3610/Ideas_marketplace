from django.db import models
from authentication.models import Employee
from django.core.validators import MaxValueValidator , MinValueValidator
from django.contrib.auth.models import Group, Permission

# Create your models here.
class Budget(models.Model):
    budget = models.FloatField()
    remaining_budget = models.FloatField()
    created_by = models.ForeignKey(Employee , on_delete=models.SET_NULL , null = True)
    set_at = models.DateTimeField(auto_now=True)



class Score(models.Model):
    creator = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feasibility = models.FloatField()
    market_value = models.FloatField()
    cost_efective = models.FloatField()
    risk = models.FloatField()
    originaity = models.FloatField()
    value_proposition = models.FloatField()




class Files(models.Model):
    file = models.FileField(upload_to='uploads/')
    employee = models.ForeignKey(Employee , on_delete=models.SET_NULL , null=True)
    


class Tags(models.Model):
    tag = models.TextField(null=False , blank=False , max_length = 100)

class Feature_Score(models.Model):
    relative_benefit = models.IntegerField(null = False , blank = False , validators=[MinValueValidator(0), MaxValueValidator(10)])
    relative_penalty = models.IntegerField(null = False , blank = False , validators=[MinValueValidator(0), MaxValueValidator(10)])
    total_value = models.IntegerField()
    relative_cost = models.IntegerField(null = False , blank = False , validators=[MinValueValidator(0), MaxValueValidator(10)])
    relative_risk = models.IntegerField(null = False , blank = False , validators=[MinValueValidator(0), MaxValueValidator(10)])
    


class Features(models.Model):
    name = models.TextField(null = False , blank = False , unique=True , max_length = 300)
    description = models.TextField(null = False, blank = False)
    feature_score = models.ForeignKey(Feature_Score , on_delete = models.SET_NULL , null=True)
    value_percentage = models.FloatField(null = True , blank = True)
    cost_percentage = models.FloatField()
    risk_percentage = models.FloatField()
    priority = models.FloatField()
    status = models.TextField(null = False , blank = False , default = "Pending" , max_length = 20)
    type = models.TextField(null = True , blank = True  , max_length = 20)
    start_date = models.DateTimeField(null = True)
    end_date = models.DateTimeField(null = True)
    
class Tasks(models.Model):
    task_title = models.TextField(null = False , blank = False , max_length=50 , unique=False)
    task_description = models.TextField(null = False , blank = False)
    assignee = models.ForeignKey(Employee , on_delete=models.SET_NULL , null=True)
    feature = models.ForeignKey(Features , on_delete=models.CASCADE)
    tag = models.TextField(max_length=30)
    start_date = models.DateTimeField(null = True)
    end_date = models.DateTimeField(null = True)


class Ideas(models.Model):
    name = models.TextField(null = False , blank = False , unique=True , max_length = 200)
    description = models.TextField(null = False, blank = False)
    problem_to_solve = models.TextField(null = True, blank = False)
    score = models.ForeignKey(Score , on_delete = models.SET_NULL , null=True)
    tags = models.ManyToManyField(Tags)
    files = models.ManyToManyField(Files)
    features = models.ManyToManyField(Features)
    created_at = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee , on_delete=models.SET_NULL , null = True)


class Projects(models.Model):
    name = models.TextField(null = False , blank = False , unique=True , max_length = 200)
    description = models.TextField(null = False, blank = False)
    problem_to_solve = models.TextField(null = True, blank = False)
    features = models.ManyToManyField(Features )
    assignee = models.ManyToManyField(Employee)
    progress = models.FloatField()
    start_date = models.DateField(null = True , blank = True)
    end_date = models.DateField(null = True , blank = True)
    tags = models.ManyToManyField(Tags)
    project_manager = models.ForeignKey(Employee , on_delete= models.SET_NULL , related_name="project_manager" , null=True)
    files = models.ManyToManyField(Files)
    tasks = models.ManyToManyField(Tasks)
    created_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null = True)
    end_date = models.DateTimeField(null = True)
    budget = models.ForeignKey(Budget , on_delete=models.PROTECT)

    
class Archived_Ideas(models.Model):
    name = models.TextField(null = False , blank = False , unique=True , max_length = 200)
    description = models.TextField(null = False, blank = False)
    problem_to_solve = models.TextField(null = True, blank = False)
    score = models.ForeignKey(Score , on_delete = models.SET_NULL , null=True)
    tags = models.ManyToManyField(Tags)
    files = models.ManyToManyField(Files)
    approved = models.BooleanField(default=False)
    archived_at = models.DateTimeField(auto_now=True)


class Archived_Projects(models.Model):
    name = models.TextField(null = False , blank = False , unique=True , max_length = 200)
    description = models.TextField(null = False, blank = False)
    problem_to_solve = models.TextField(null = True, blank = False)
    features = models.ForeignKey(Features , on_delete = models.SET_NULL , null = True)
    assignee = models.ManyToManyField(Employee)
    progress = models.FloatField()
    start_date = models.DateField(null = True , blank = True)
    end_date = models.DateField(null = True , blank = True)
    tags = models.ManyToManyField(Tags)
    project_manager = models.ForeignKey(Employee , on_delete= models.SET_NULL , related_name="project_manager_was" , null=True)
    files = models.ManyToManyField(Files)
    archived_at = models.DateTimeField(auto_now=True)





score_permission = Permission.objects.get(codename='add_score')


hr_group = Group.objects.get(name='HR')
hr_group.permissions.add(score_permission)
marketing_group = Group.objects.get(name='Marketing')
marketing_group.permissions.add(score_permission)
