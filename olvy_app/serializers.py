from asyncore import file_dispatcher
from curses import meta
from dataclasses import field
from rest_framework import serializers
from .models import user,review,product
import datetime

class UserSerialzer(serializers.ModelSerializer):
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    class Meta:
        model=user
        fields='__all__'


class ReviewSerializer(serializers.ModelSerializer):
    reviewerName=serializers.CharField(source='reviewerID.user_name')
    unixReviewTime = serializers.IntegerField()

    class Meta:
        model=review
        fields='__all__'

    def to_representation(self, data):
        data = super(ReviewSerializer, self).to_representation(data)
        get_date= datetime.datetime.fromtimestamp(data['unixReviewTime'])
        datetime_str = get_date.strftime( "%m - %d - %Y ")  
        data['unixReviewTime'] =datetime_str
        return data

class ProductSerializer(serializers.ModelSerializer):
    product_id=serializers.CharField()  
    ratings = serializers.JSONField()

    class Meta:
        model=product
        fields='__all__'