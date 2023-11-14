from rest_framework import serializers
from course.models import Course,Category,SubCategory,Tags,Module,FavouriteCourses
from accounts.models import StudentProfile




class CourseSerializerHome(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(source='instructor.user.first_name', read_only=True)
    instructor_last_name = serializers.CharField(source='instructor.user.last_name', read_only=True)
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        depth = 1

    def get_is_favourite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            student = StudentProfile.objects.get(user=user)
            return FavouriteCourses.objects.filter(student=student, course=obj).exists()
        return False    


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, source='tags_set')
    class Meta:
        model = SubCategory
        fields = '__all__'



class CategorySubcategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, source='subcategory_set')
    class Meta:
        model = Category
        fields = '__all__'   



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'        


class CourseDetailSerializer(serializers.ModelSerializer):
    instructor_first_name = serializers.CharField(source='instructor.user.first_name', read_only=True)
    instructor_last_name = serializers.CharField(source='instructor.user.last_name', read_only=True)
    instructor_bio = serializers.CharField(source='instructor.bio', read_only=True)
    instructor_skill = serializers.CharField(source='instructor.skill', read_only=True)
    instructor_photo = serializers.FileField(source='instructor.profile_photo', read_only=True)
    modules = ModuleSerializer(many=True, source='module_set')

    class Meta:
        model = Course
        fields = '__all__'


class FavouriteCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteCourses
        fields = '__all__'
