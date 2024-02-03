from django.db import models
from authentication.models import Employee
from django.core.validators import MaxValueValidator , MinValueValidator
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

def validate_minmax(value):
    if value < 0 or value > 1:
        raise ValidationError("Weight must be between 0 and 1" , params={"value":value},)
def validate_score_minmax(value):
    if value < 0 or value > 10:
        raise ValidationError("Weight must be between 0 and 10" , params={"value":value},)
    
def validate_sum_to_one(value):
    if value != 1:
        raise ValidationError("The sum of all weights must be equal to 1.")

def validate_sumValues_to_one(value):
    if value >= 0.9 and value <= 1:
        raise ValidationError("The sum of all values must be equal to 1.")
# Create your models here.
class Budget(models.Model):
    budget = models.FloatField()
    remaining_budget = models.FloatField()
    created_by = models.ForeignKey(Employee , on_delete=models.SET_NULL , null = True)
    set_at = models.DateTimeField(auto_now=True)








class Files(models.Model):
    file = models.FileField(upload_to='uploads/')
    employee = models.ForeignKey(Employee , on_delete=models.SET_NULL , null=True)
    


class Tags(models.Model):
    tag = models.TextField(null=False , blank=False , max_length = 100)

class FeatureScore(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    relative_benefit = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(10)])
    relative_penalty = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(10)])
    total_value = models.IntegerField()
    relative_cost = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(10)])
    relative_risk = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(10)])
    priority = models.FloatField(null=True)  # New field for priority

    def calculate_feature_score(self, weight_benefit, weight_penalty, weight_total_value, weight_cost, weight_risk):
        weighted_sum = (
            weight_benefit * self.relative_benefit +
            weight_penalty * self.relative_penalty +
            weight_total_value * self.total_value +
            weight_cost * self.relative_cost +
            weight_risk * self.relative_risk
        )
        normalized_score_out_of_50 = (weighted_sum / 10) * 50
        self.priority = normalized_score_out_of_50  # Assign the priority to the new field
        return normalized_score_out_of_50


class Features(models.Model):
    name = models.TextField(null=False, blank=False, unique=True, max_length=300)
    description = models.TextField(null=False, blank=False)
    feature_score = models.OneToOneField(FeatureScore, null=True, on_delete=models.SET_NULL)
    value_percentage = models.FloatField(null=True, blank=True)
    cost_percentage = models.FloatField(null=True, blank=True)
    risk_percentage = models.FloatField(null=True, blank=True)
    priority = models.FloatField(null=True, blank=True)
    status = models.TextField(null=False, blank=False, default="Pending", max_length=20)
    type = models.TextField(null=True, blank=True, max_length=20)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    @property
    def weighted_prioritization_matrix(self):
        # Define your weights based on the prioritization matrix
        weight_benefit = 0.3
        weight_penalty = 0.1
        weight_total_value = 0.2
        weight_cost = 0.2
        weight_risk = 0.2

        # Calculate feature score using FeatureScore model
        feature_score_instance = FeatureScore(
            relative_benefit=self.value_percentage,
            relative_penalty=self.cost_percentage,
            total_value=0,  # Adjust based on your business logic
            relative_cost=self.cost_percentage,
            relative_risk=self.risk_percentage
        )

        # Calculate feature score and save the instance
        feature_score_instance.save()

        # Use the feature score to calculate other percentages and priority
        self.value_percentage = feature_score_instance.calculate_feature_score(
            weight_benefit, weight_penalty, weight_total_value, weight_cost, weight_risk
        )

        # Save the feature score in the Features model
        self.feature_score = feature_score_instance
        self.cost_percentage = self.feature_score.relative_cost  # Assign cost percentage from feature_score
        self.risk_percentage = self.feature_score.relative_risk  # Assign risk percentage from feature_score
        self.priority = self.feature_score.priority

        return {
            'value_percentage': self.value_percentage,
            'cost_percentage': self.cost_percentage,
            'risk_percentage': self.risk_percentage,
            'priority': self.priority,
        }
    
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
    tags = models.ManyToManyField(Tags)
    files = models.ManyToManyField(Files)
    features = models.ManyToManyField(Features)
    created_at = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee , on_delete=models.SET_NULL , null = True)
    total_score = models.FloatField(default=0.0)  # Default to 0.0, you can adjust as needed

    

class Score(models.Model):
    creator = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feasibility = models.FloatField(validators=[validate_score_minmax])
    market_value = models.FloatField(validators=[validate_score_minmax])
    cost_effective = models.FloatField(validators=[validate_score_minmax])
    risk = models.FloatField(validators=[validate_score_minmax])
    originality = models.FloatField(validators=[validate_score_minmax])
    value_proposition = models.FloatField(validators=[validate_score_minmax])
    total_score = models.FloatField(default=0.0)  # Default to 0.0, you can adjust as needed
    idea = models.ForeignKey(Ideas, on_delete=models.SET_NULL, null=True)
    FEASIBILITY_WEIGHT = models.FloatField(default=0.2, validators=[validate_minmax])
    MARKET_VALUE_WEIGHT = models.FloatField(default=0.3, validators=[validate_minmax])
    COST_EFFECTIVE_WEIGHT = models.FloatField(default=0.1, validators=[validate_minmax])
    RISK_WEIGHT = models.FloatField(default=0.15, validators=[validate_minmax])
    ORIGINALITY_WEIGHT = models.FloatField(default=0.1, validators=[validate_minmax])
    VALUE_PROPOSITION_WEIGHT = models.FloatField(default=0.15, validators=[validate_minmax])

    def clean(self):
        # Validate that the sum of all weights equals 1
        total_weight = (
            self.FEASIBILITY_WEIGHT +
            self.MARKET_VALUE_WEIGHT +
            self.COST_EFFECTIVE_WEIGHT +
            self.RISK_WEIGHT +
            self.ORIGINALITY_WEIGHT +
            self.VALUE_PROPOSITION_WEIGHT
        )
        validate_sum_to_one(total_weight)

    
    
    @property
    def calculate_total_score(self):
        total_score = (
            self.feasibility/ 10 * self.FEASIBILITY_WEIGHT +
            self.market_value / 10 * self.MARKET_VALUE_WEIGHT +
            self.cost_effective /10 * self.COST_EFFECTIVE_WEIGHT +
            self.risk / 10 * self.RISK_WEIGHT +
            self.originality /10* self.ORIGINALITY_WEIGHT +
            self.value_proposition /10 * self.VALUE_PROPOSITION_WEIGHT
        )
        total_score = min(max(total_score, 0), 1)
        
        return round(total_score * 100, 1)
    def save(self, *args, **kwargs):
        # Calculate and save the total score before saving the object
        self.total_score = self.calculate_total_score
        score = Ideas.objects.get(pk = self.idea.id)
        score.total_score = self.total_score
        score.save()
        

        super().save(*args, **kwargs)


class ScoreManager(models.Manager):
    def calculate_average_score(self, idea):
        # Calculate the average score for a given idea
        total_scores = 0
        num_employees = 0

        # Get all scores for the idea
        idea_scores = self.filter(idea=idea)

        for score in idea_scores:
            total_scores += score.calculate_total_score()
            num_employees += 1

        if num_employees == 0:
            return 0  

        average_score = total_scores / num_employees
        return average_score

class Projects(models.Model):
    name = models.TextField(null = False , blank = False , unique=True , max_length = 200)
    description = models.TextField(null = False, blank = False)
    problem_to_solve = models.TextField(null = True, blank = False)
    features = models.ManyToManyField(Features)
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





# score_permission = Permission.objects.get(codename='add_score')


# hr_group = Group.objects.get(name='HR')
# hr_group.permissions.add(score_permission)
# marketing_group = Group.objects.get(name='Marketing')
# marketing_group.permissions.add(score_permission)
