from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,PostSerializer,LikeSerializer
from rest_framework import authentication,permissions,status,viewsets
from rest_framework.viewsets import ModelViewSet,ViewSet
from api.models import Users,Post,Like
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound




# Create your views here.





class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
        
class PostView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = PostSerializer
    
    def create(self,request,*args,**kwargs):
        serializer=PostSerializer(data=request.data)
        user_id=request.user.id
        print(user_id)
        user_object=Users.objects.get(id=user_id)
        if user_object:
            if serializer.is_valid():
                serializer.save(user=user_object)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(request,"user not found")

    @action(methods=['patch'], detail=True, url_path='publish')
    def publish(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if post.user.id != request.user.id:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        is_published = request.data.get('is_published')
        if is_published is None:
            return Response({"detail": "'is_published' field is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(is_published, bool):
            return Response({"detail": "'is_published' must be a boolean"}, status=status.HTTP_400_BAD_REQUEST)
        
        post.is_published = is_published
        post.save()

        serializer = PostSerializer(post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        
    

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(is_published=True)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)    
        
    def destroy(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        try:
            post_obj = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if post_obj.user.id != request.user.id:
            return Response({"detail": "You do not have permission to delete this post"}, status=status.HTTP_403_FORBIDDEN)

        post_obj.delete()
        return Response({"detail": "Post deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        
        
    @action(methods=["post"], detail=True, url_path='like')
    def like(self, request, pk=None):
        serializer = LikeSerializer(data=request.data)
        try:
            post_obj = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user.id
        try:
            user_object = Users.objects.get(id=user)
        except Users.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if Like.objects.filter(post=post_obj, user=user_object).exists():
            return Response({"detail": "User already liked this post"}, status=status.HTTP_400_BAD_REQUEST)    

        if serializer.is_valid():
            serializer.save(post=post_obj, user=user_object)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
class LikeView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=LikeSerializer
    def destroy(self, request, *args, **kwargs):
        like_id = kwargs.get('pk')
        try:
            like_obj = Like.objects.get(id=like_id)
        except Like.DoesNotExist:
            return Response({"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

        if like_obj.user.id != request.user.id:
            return Response({"detail": "You do not have permission to delete this like"}, status=status.HTTP_403_FORBIDDEN)
        like_obj.delete()
        return Response({"detail": "Like deleted successfully"},status=status.HTTP_204_NO_CONTENT)