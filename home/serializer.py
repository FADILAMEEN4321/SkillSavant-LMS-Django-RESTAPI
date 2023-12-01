from rest_framework import serializers
from course.models import Course, Category, SubCategory, Tags, Module, FavouriteCourses
from accounts.models import StudentProfile
from enrollment.models import ModuleProgress


class CourseSerializerHome(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(
        source="instructor.user.first_name", read_only=True
    )
    instructor_last_name = serializers.CharField(
        source="instructor.user.last_name", read_only=True
    )
    is_favourite = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        depth = 1

    def get_is_favourite(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            student = StudentProfile.objects.get(user=user)
            return FavouriteCourses.objects.filter(student=student, course=obj).exists()
        return False

    def get_duration(self, obj):
        return obj.total_duration()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, source="tags_set")

    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySubcategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, source="subcategory_set")

    class Meta:
        model = Category
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = "__all__"

    def get_is_completed(self, module):
        # Check if there is a ModuleProgress record for the current user and module
        user = self.context["request"].user
        if user.is_authenticated:
            try:
                module_progress = ModuleProgress.objects.get(
                    module=module, student=user.studentprofile
                )
                return module_progress.is_completed
            except ModuleProgress.DoesNotExist:
                return False
        return False


class CourseDetailSerializer(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(
        source="instructor.user.first_name", read_only=True
    )
    instructor_last_name = serializers.CharField(
        source="instructor.user.last_name", read_only=True
    )
    instructor_bio = serializers.CharField(source="instructor.bio", read_only=True)
    instructor_skill = serializers.CharField(source="instructor.skill", read_only=True)
    instructor_photo = serializers.FileField(
        source="instructor.profile_photo", read_only=True
    )
    modules = ModuleSerializer(many=True, source="module_set")
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_duration(self, course):
        return course.total_duration()


class FavouriteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCourses
        fields = "__all__"


class FavouriteCourseListingSerializer(serializers.ModelSerializer):
    course_details = CourseSerializerHome(source="course", read_only=True)

    class Meta:
        model = FavouriteCourses
        fields = ["added_at", "course_details", "id"]
