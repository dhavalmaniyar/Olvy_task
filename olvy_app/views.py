from traceback import print_tb
from django.shortcuts import render
import datetime
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *


class UserList(APIView):
    def get(self, request):
        user_list = user.objects.all()
        serialize = UserSerialzer(user_list, many=True)
        return Response(serialize.data)

    def post(self, request):
        serializer = UserSerialzer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ReviewList(APIView):
    def get(self, request):
        preferred_by = request.GET.get('preference')
        filter_by = request.GET.get('asin')

        if filter_by and preferred_by == 'mostrecent':
            review_list = review.objects.filter(
                asin=filter_by).order_by('-unixReviewTime')

        elif filter_by and preferred_by == 'topreview':
            review_list = review.objects.filter(
                asin=filter_by).order_by('-helpful')

        elif preferred_by == 'mostrecent':
            review_list = review.objects.all().order_by('-unixReviewTime')

        elif filter_by:
            review_list = review.objects.filter(
                asin=filter_by).order_by('-helpful')
        else:
            review_list = review.objects.all().order_by('-helpful')

        if preferred_by == 'mostrecent' and filter_by == 'All Data':
            review_list = review.objects.all().order_by('-unixReviewTime')

        if preferred_by == 'topreview' and filter_by == 'All Data':
            review_list = review.objects.all().order_by('-helpful')

        if filter_by == "All Data" and preferred_by == "":
            review_list = review.objects.all().order_by('-helpful')

        serializer = ReviewSerializer(review_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        for data in request.data:
            user_details = {
                'user_id': data['reviewerID'], 'user_name': data['reviewerName']}
            serialize_user = UserSerialzer(data=user_details)
            if not user.objects.filter(user_id=data['reviewerID']).exists():
                if serialize_user.is_valid():
                    serialize_user.save()
            reviewSummary = {
                '1': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
            }
            product_details = {
                'product_id': data['asin'], 'ratings': reviewSummary}
            serialize_product = ProductSerializer(data=product_details)
            productEntry = product.objects.filter(product_id=data['asin'])
            print(type(productEntry))
            if productEntry.exists():
                print("NOT EXIXT")
                productObj = productEntry[0]
                productObj.ratings[data['overall']] += 1
                productObj.save()
            elif serialize_product.is_valid():
                print("EXITST")
                productEntry = serialize_product.save()
                productEntry.ratings[data['overall']] += 1
                productEntry.save()

            vote = data['helpful'][0]
            data['helpful'] = vote
            serialize_review = ReviewSerializer(data=data)
            if serialize_review.is_valid():
                serialize_review.save()


class ProductList(APIView):
    def get(self, request):
        product_list = product.objects.all()
        serializer = ProductSerializer(product_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status.HTTP_200_OK)
