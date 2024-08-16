from rest_framework import serializers
from .models import Users,Post,Like



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=["id","username","email_id","password","phone_number","name"]
        
    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)
    
    
    
class PostSerializer(serializers.ModelSerializer):
    # user_has_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'tags', 'created_at', 'is_published', 'like_count']

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        return Like.objects.filter(post=obj, user=user).exists()

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()
    
    
class LikeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_at=serializers.CharField(read_only=True)
    class Meta:
        model = Like
        fields=['id','user','created_at']