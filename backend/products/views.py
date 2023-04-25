from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# from django.http import Http404

from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  
  def perform_create(self, serializer):
    # serializer.save(user=self.request.user)
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    if content is None:
      content = title
    print(serializer.validated_data)
    serializer.save(content=content)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  # lookup_field = 'pk'
  
product_detail_view = ProductDetailAPIView.as_view()



class ProductUpdateAPIView(generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = 'pk'
  
  def perform_update(self, serializer):
    instance = serializer.save()
    if not instance.content:
      instance.content = instance.title
  
product_update_view = ProductUpdateAPIView.as_view()



class ProductDestroyAPIView(generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = 'pk'
  
  def perform_destroy(self, instance):
    # instance
    super().perform_destroy(instance)
  
product_destroy_view = ProductDestroyAPIView.as_view()



class ProductListAPIView(generics.ListAPIView):
  '''
  Not gonna use this method
  '''
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  
product_list_view = ProductListAPIView.as_view()




class ProductMixinView(generics.GenericAPIView)





@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
  method = request.method
  
  if method == 'GET':
    if pk is not None:
      # detail view
      obj = get_object_or_404(Product, pk=pk)
      data = ProductSerializer(obj, many=False).data
      return Response(data)
    
    # list view
    queryset = Product.objects.all()
    data = ProductSerializer(queryset, many=True).data
    return Response(data)
  
  if method == 'POST':
    # create an item
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      title = serializer.validated_data.get('title')
      content = serializer.validated_data.get('content') or None
      if content is None:
        content = title
      serializer.save(content=content)
      return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400)
  
  
  