from django.shortcuts import get_object_or_404, render
from .models import Product,ProductImages, Review
from .serializers import ProductSerializer,ProductImageSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .filters import ProductsFilter
from rest_framework import status
from django.db.models import Avg

from rest_framework.permissions import IsAuthenticated,IsAdminUser

@api_view(["GET"])#api/products
def get_product(request):
    # product = Product.objects.all()#queryset to get all data
    filterset = ProductsFilter(
        request.GET,queryset=Product.objects.all().order_by('id'))
    serializer  = ProductSerializer(filterset.qs,many=True)#converting it to serializer which is json converter
    return Response({"product":serializer.data})


@api_view(["GET"])#api/products/id
def get_product_individual(request,pk):
    product_detail = get_object_or_404(Product,id=pk)#queryset to get all data
    serializer  = ProductSerializer(product_detail,many=False)#converting it to serializer which is json converter
    return Response({"product_detail":serializer.data})

@api_view(["POST"])#api/products/new_product/
@permission_classes([IsAuthenticated])
def new_product(request):

    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
         product = Product.objects.create(**data,user=request.user)
         res = ProductSerializer(product,many=False)
         return Response({"product":res.data})
    else:
        return Response(serializer.errors)





@api_view(["POST"])#api/products/images/
def upload_images(request):

    data = request.data
    files = request.FILES.getlist('images')

    images = []
    for f in files:
        image = ProductImages.objects.create(product=Product(data['product']),image=f)
        images.append(image)
    serializer = ProductImageSerializer(images,many=True)

    return Response(serializer.data)



@api_view(["PUT"])#api/products/id/update
@permission_classes([IsAuthenticated])
def update_product(request,pk):
    product = get_object_or_404(Product,id=pk)

    if product.user != request.user:
        return Response({'error':'You Cannot Update This Product'},status=status.HTTP_403_FORBIDDEN)

    product.name=request.data['name']
    product.description=request.data['description']
    product.price=request.data['price']
    product.category=request.data['category']
    product.brand=request.data['brand']
    product.ratings=request.data['ratings']
    product.srock=request.data['srock']

    product.save()

    serializer = ProductSerializer(product,many=False)

    return Response({"product":serializer.data})


@api_view(["DELETE"])#api/products/id/delete/
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({'error':'You Cannot Delete This Product'},status=status.HTTP_403_FORBIDDEN)

    args = {"product":pk}
    images = ProductImages.objects.filter(*args)
    for i in images:
        i.delete()
    product.delete()
    return Response({'detils':'Product Delete Succesfully'},status=status.HTTP_200_OK)




@api_view(["POST"])  # This function will only accept POST requests.
@permission_classes([IsAuthenticated])  #  Ensures only authenticated users can access this view.
def create_review(request, pk):

    user = request.user  #  Gets the currently logged-in user.
    product = get_object_or_404(Product, id=pk)  #  Fetches the product by ID; returns 404 if not found.
    data = request.data  #  Retrieves data sent from the client in the request body.

    #  Checks if the user has already reviewed this product
    review = product.reviews.filter(user=user)  # (Assumes `related_name="reviews"` is set in Review model)

    #  Validate that the rating is between 1 and 5
    if data['ratings'] <= 0 or data['ratings'] > 5:  
        return Response({'error': 'Please Select Rating Between 1-5'}, status=status.HTTP_400_BAD_REQUEST)

    #  If the review exists, update it
    elif review.exists():
        new_review = {'ratings': data['ratings'], 'comment': data['comment']}  #  Updated values
        review.update(**new_review)  #  Updates the existing review with new values

        #  Calculate and update the product's average rating
        rating = product.reviews.aggregate(avg_ratings=Avg('ratings'))  # Aggregates all reviews' ratings
        product.ratings = rating['avg_ratings']  # Updates product's ratings field
        product.save()  # Saves the updated rating in the database

        return Response({'detail': 'Review Updated'})  # Returns success message

    #  If no existing review, create a new one
    else:
        Review.objects.create(
            user=user,  #  Assigns the current user to the review
            product=product,  #  Associates the review with the product
            ratings=data['ratings'],  #  Saves the rating from request data
            comment=data['comment']  #  Saves the comment from request data
        )

        #  Calculate and update the product's average rating after the new review
        rating = product.reviews.aggregate(avg_ratings=Avg('ratings'))  
        product.ratings = rating['avg_ratings']  #  Updates the product's overall rating
        product.save()  #  Saves the updated product data

        return Response({'detail': 'Review Posted'})  #  Returns success message

   
@api_view(["DELETE"])  #  Accepts DELETE requests only
@permission_classes([IsAuthenticated,IsAdminUser])  #  Only authenticated users can delete reviews
def delete_review(request, pk):
    user = request.user  #  Gets the currently logged-in user
    product = get_object_or_404(Product, id=pk)  #  Fetches the product by ID
    review = Review.objects.filter(user=user, product=product).first()  #  Finds the review by user & product

    if not review:  
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)  #  If no review found

    review.delete()  #  Deletes the review

    #  Recalculate the average rating for the product
    rating = product.reviews.aggregate(avg_ratings=Avg('ratings'))
    product.ratings = rating['avg_ratings'] if rating['avg_ratings'] is not None else 0  #  Update or set to 0
    product.save()  #  Save updated rating

    return Response({'detail': 'Review Deleted'}, status=status.HTTP_200_OK)  #  Return success response
