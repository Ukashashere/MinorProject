# from django.db import models

# class User(models.Model):
#     email = models.EmailField(max_length=254, unique=True, primary_key=True)
#     password = models.CharField(max_length=300)
#     user_created = models.DateTimeField(auto_now_add=True)
#     user_updated = models.DateTimeField(auto_now=True)    
#     name = models.CharField(max_length=80, default='')
#     age = models.IntegerField(default=0)
#     sex = models.CharField(max_length=10, null=True, blank=True)
#     height_inches = models.FloatField(null=True, blank=True)
#     weight = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return self.email

# class PoseAnalysis(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
#     shoulder_width_in = models.FloatField()
#     chest_circumference_in = models.FloatField()
#     waist_width_in = models.FloatField()
#     waist_circumference_in = models.FloatField()
#     hip_width_in = models.FloatField()
#     hip_circumference_in = models.FloatField()
#     biceps_left_length_in = models.FloatField()
#     biceps_right_length_in = models.FloatField()
#     biceps_left_circumference_in = models.FloatField()
#     biceps_right_circumference_in = models.FloatField()
#     forearm_left_length_in = models.FloatField()
#     forearm_right_length_in = models.FloatField()
#     forearm_left_circumference_in = models.FloatField()
#     forearm_right_circumference_in = models.FloatField()
#     thigh_left_length_in = models.FloatField()
#     thigh_right_length_in = models.FloatField()
#     thigh_left_circumference_in = models.FloatField()
#     thigh_right_circumference_in = models.FloatField()
#     calf_left_length_in = models.FloatField()
#     calf_right_length_in = models.FloatField()
#     calf_left_circumference_in = models.FloatField()
#     calf_right_circumference_in = models.FloatField()

#     def __str__(self):
#         return f"Pose analysis for {self.user.email}"


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    height_inches = models.DecimalField(max_digits=4, decimal_places=1)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    user_created = models.DateTimeField(default=timezone.now)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age', 'sex', 'height_inches', 'weight_kg']

    def __str__(self):
        return self.email
    

class VideoUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_uploads')
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    result = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.user.email}'s video - {self.uploaded_at}"

class ExerciseLog(models.Model):
    video = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name='exercise_logs')
    exercise = models.CharField(max_length=100)
    reps = models.IntegerField()
    timing = models.FloatField()
    incorrect_reps = models.IntegerField()

    def __str__(self):
        return f"{self.video.user.email}'s {self.exercise} - {self.reps} reps"

    @property
    def user(self):
        return self.video.user

class RepDetail(models.Model):
    exercise_log = models.ForeignKey(ExerciseLog, on_delete=models.CASCADE, related_name='rep_details')
    rep_count = models.IntegerField()
    is_correct = models.BooleanField()
    duration = models.FloatField()

    def __str__(self):
        return f"Rep {self.rep_count} for {self.exercise_log.exercise}"

    @property
    def user(self):
        return self.exercise_log.video.user

class BodyMeasurements(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    measurement_date = models.DateTimeField(auto_now_add=True)
    
    # Width measurements
    shoulder_width_in = models.FloatField()
    waist_width_in = models.FloatField()
    hip_width_in = models.FloatField()
    
    # Circumference measurements
    chest_circumference_in = models.FloatField()
    waist_circumference_in = models.FloatField()
    hip_circumference_in = models.FloatField()
    
    # Left side measurements
    biceps_left_length_in = models.FloatField()
    biceps_left_circumference_in = models.FloatField()
    forearm_left_length_in = models.FloatField()
    forearm_left_circumference_in = models.FloatField()
    thigh_left_length_in = models.FloatField()
    thigh_left_circumference_in = models.FloatField()
    calf_left_length_in = models.FloatField()
    calf_left_circumference_in = models.FloatField()
    
    # Right side measurements
    biceps_right_length_in = models.FloatField()
    biceps_right_circumference_in = models.FloatField()
    forearm_right_length_in = models.FloatField()
    forearm_right_circumference_in = models.FloatField()
    thigh_right_length_in = models.FloatField()
    thigh_right_circumference_in = models.FloatField()
    calf_right_length_in = models.FloatField()
    calf_right_circumference_in = models.FloatField()

     # Current measurement
    weight_kg = models.FloatField()
    
    trunk_to_leg_ratio = models.FloatField()
    body_fat_percentage = models.FloatField()
    fat_mass = models.FloatField()
    lean_mass = models.FloatField()
    waist_circumference = models.FloatField()
    waist_to_hip_ratio = models.FloatField()
    skeletal_muscle_mass = models.FloatField()
    fat_free_mass = models.FloatField()
    basal_metabolic_rate = models.FloatField()
    visceral_fat_level = models.FloatField()
    bmi = models.FloatField()
    class Meta:
        ordering = ['-measurement_date']


class NutritionRequirements(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    calculation_date = models.DateTimeField(auto_now_add=True)
    calories = models.CharField(max_length=50)  # Store as string to preserve exact format
    protein = models.CharField(max_length=50)   # Store as string to preserve exact format

    class Meta:
        ordering = ['-calculation_date']