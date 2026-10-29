from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics

from .models import *
from .serializers import *
from .utils import *
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            subject = 'You are registered in Happy Couple Solution'
            message = f"""
            Your account has been created successfully
            your email is: {serializer.validated_data['email']}
            your username is: {serializer.validated_data['email']}
            """
            from_email = 'happycouplesolution@gmail.com'
            recipient_list = [serializer.validated_data['email']]
            refresh = RefreshToken.for_user(User.objects.get(email=serializer.validated_data['email']))
            
            return Response({'message': 'Account verified and created successfully',
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                             }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(APIView):
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
    

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    def post(self, request):
        username = request.data.get('email')
        email = request.data.get('email')

        if not username or not email:
            return Response({'error': 'Username and email are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create the user based on the provided email
        user, created = User.objects.get_or_create(email=email, defaults={'username': email})

        # If the user was just created, you can assign the username or handle further logic here
        if created:
            user.username = username
            googl_auth_login_mail(email, user.username)
            user.save()
        

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)



class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })



class BoxModelViewSet(APIView):
    pagination_class = CustomPagination
    
    def get(self, request, *args, **kwargs):
        boxes = BoxModel.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(boxes, request, view=self)

        serializer = BoxModelSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        sizes_data = request.data.pop('sizes', None)  # Extract sizes before saving BoxModel
        serializer = BoxModelSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            box = serializer.save()  # Save the BoxModel first
            
            # Save related sizes if provided
            if sizes_data:
                for size_data in sizes_data:
                    size_data['box'] = box.id  # Link the size to the box
                    size_serializer = BoxSizeModelSerializer(data=size_data, context={'request': request})
                    if size_serializer.is_valid():
                        size_serializer.save()
                    else:
                        # If size data invalid → rollback and delete the box
                        box.delete()
                        return Response({
                            "error": "Invalid size data",
                            "details": size_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)
            
            final_data = BoxModelSerializer(box, context={'request': request}).data
            return Response(final_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BoxSingleView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({'error': 'Box ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            box = BoxModel.objects.get(id=id)
            serializer = BoxModelSerializer(box, context={'request': request})
            return Response(serializer.data)
        except BoxModel.DoesNotExist:
            return Response({'error': 'Box not found'}, status=status.HTTP_404_NOT_FOUND)


class ContactView(APIView):
    """
    API view to submit contact enquiries and optionally retrieve them.
    - POST: Saves the contact enquiry and sends:
        1. An enquiry notification email to info2easypack@gmail.com
        2. A confirmation/acknowledgement reply email to the customer
    - GET: Retrieves list of contact enquiries.
    """
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            # Send email to info2easypack@gmail.com and acknowledgement reply to the customer
            email_status = send_contact_emails(
                name=contact.name,
                email=contact.email,
                subject=contact.subject,
                message=contact.message,
                phone_number=contact.phone_number
            )

            return Response({
                'message': 'Your contact enquiry has been submitted successfully.',
                'email_status': email_status,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        contacts = Contact.objects.all().order_by('-created_at')
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
