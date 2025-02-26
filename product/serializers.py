from rest_framework import serializers
from .models import Product,ProductImages, Review



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    images=ProductImageSerializer(many=True,read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews',read_only=True)

    class Meta:
        model = Product
        fields = ['id','name','description','price','brand','category','srock','user','images','reviews']


    #validation

    extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'price': {'required': True, 'min_value': 1},
            
        }
    def validate_name(self, value):
        if not value.strip():  # Prevent empty strings or spaces
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    def validate_images(self, value):
        if not value:
            raise serializers.ValidationError("At least one image is required.")
        return value
#reviews display in product also update upper section of reviews  
    def get_reviews(self,obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews,many=True)
        return serializer.data



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"