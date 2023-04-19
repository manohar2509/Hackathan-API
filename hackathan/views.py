from django.shortcuts import render
from rest_framework.views import APIView
from authenticate.models import User
from .models import Hackathon, Registration, Submission
from .serializers import HackathonSerializer, RegistrationSerializer, SubmissionSerializer
from rest_framework.response import Response
import jwt,datetime
from .constants import messages, filetypes



def add_user_to_request_data(request,user):
    req = request.data.copy()
    req['user'] = user.id
    return req

def validate_user(request):
    if 'jwt' not in request.headers:
        return None
    token = request.headers['jwt']
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        return None
    user = User.objects.filter(id=payload['id']).first()
    if user is None:
        return None
    return user

def validate_submission(request, hackathon):
    submission_type = hackathon.submission_type
    
    if submission_type == 'image':
        if request.data.get('image_submission', None) is None:
            return {'status': messages.FAILURE, 'data': submission_type + messages.IS_REQUIRED}
        elif not request.data['image_submission'].content_type.startswith(filetypes.IMAGE):
            return {'status': messages.FAILURE, 'data': submission_type + messages.FORMAT_NOT_SUPPORTED}
        else:
            request.data['file_submission'] = None
            request.data['link_submission'] = None
            return None
    
    if submission_type == 'file':
        if request.data.get('file_submission', None) is None:
            return {'status': messages.FAILURE, 'data': submission_type + messages.IS_REQUIRED}
        elif not request.data['file_submission'].content_type.startswith(filetypes.APPLICATION):
            return {'status': messages.FAILURE, 'data': submission_type + messages.FORMAT_NOT_SUPPORTED}
        else:
            request.data['image_submission'] = None
            request.data['link_submission'] = None
            return None
    
    if submission_type == 'link':
        if request.data.get('link_submission', None) is None:
            return {'status': messages.FAILURE, 'data': submission_type + messages.IS_REQUIRED}
        elif not request.data['link_submission'].startswith(filetypes.LINK):
            return {'status': messages.FAILURE, 'data': submission_type + messages.FORMAT_NOT_SUPPORTED}
        else:
            request.data['image_submission'] = None
            request.data['file_submission'] = None
            return None

def submit_to_hackathon(request, user):

    hackathon_id = request.data['hackathon']
    hackathon = Hackathon.objects.filter(id=hackathon_id).first()
    if hackathon is None:
        return {'error': 'invalid hackathon id', 'status': messages.FAILURE}
    
    registration = Registration.objects.filter(user=user, hackathon=hackathon).first()
    if registration is None:
        return {'error': 'user not registered to hackathon', 'status': messages.FAILURE}
    
    submission_error = validate_submission(request, hackathon)
    if submission_error:
        return submission_error

    req = add_user_to_request_data(request,user)

    serializer = SubmissionSerializer(data=req)
    if not serializer.is_valid():
        return {'status': messages.FAILURE, 'error': serializer.errors}
    
    serializer.save()
    return {'status': messages.SUCCESS, 'data': serializer.data}

class CreateHackathan(APIView):
    def post(self,request):
        user = validate_user(request)
        if not user:
            return Response({'error': messages.INVALID_TOKEN, 'status': messages.FAILURE})
        req = add_user_to_request_data(request,user)
        serializer=HackathonSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':messages.SUCCESS,'data':serializer.data})
        return Response({'status':messages.FAILURE,'error':serializer.errors})



class GetHackathons(APIView):
    def get(self,request):
        hackathons = Hackathon.objects.all()
        serializer = HackathonSerializer(hackathons, many=True)
        return Response(serializer.data)

class RegistrationToHackathan(APIView):
    def post(self,request):
        user = validate_user(request)
        if not user:
            return Response({'error': messages.INVALID_TOKEN, 'status': messages.FAILURE})
        req = add_user_to_request_data(request,user)
        serializer=RegistrationSerializer(data=req)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':messages.SUCCESS,'data':serializer.data})
        return Response({'status':messages.FAILURE,'error':serializer.errors})
class GetRegistrations(APIView):
    def get(self,request):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

class CreateSubmission(APIView):
    def post(self,request):
        user = validate_user(request)
        if not user:
            return Response({'error': messages.INVALID_TOKEN, 'status': messages.FAILURE})
        response = submit_to_hackathon(request, user)
        return Response(response)


class GetRegisteredHackathons(APIView):
    def get(self,request):
        user = validate_user(request)
        if not user:
            return Response({'error': messages.INVALID_TOKEN, 'status': messages.FAILURE})
        req = add_user_to_request_data(request,user)
        user = User.objects.filter(id=req['user']).first()
        registrations = Registration.objects.filter(user=user)
        hackathons = []
        for registration in registrations:
            hackathons.append(registration.hackathon)
        serializer = HackathonSerializer(hackathons, many=True)
        return Response(serializer.data)


class GetSubmissions(APIView):
    def get(self,request):
        user = validate_user(request)
        if not user:
            return Response({'error': messages.INVALID_TOKEN, 'status': messages.FAILURE})
        req = add_user_to_request_data(request,user)
        user = User.objects.filter(id=req['user']).first()
        submissions = Submission.objects.filter(user=user)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
