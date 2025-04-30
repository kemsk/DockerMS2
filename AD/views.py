import json
import jwt
import logging
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework import status
from rest_framework_simplejwt.backends import TokenBackend
from .models import StudentData

# ------------------------ LOGGING SETUP ------------------------

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------------ JWT DECORATOR ------------------------

def jwt_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("401 Unauthorized: Missing or invalid auth header")
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)
        token = auth_header.split(" ")[1]
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            request.user_payload = decoded
        except jwt.ExpiredSignatureError:
            logger.warning("401 Unauthorized: Token expired")
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            logger.warning("401 Unauthorized: Invalid token")
            return JsonResponse({"error": "Invalid token"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped_view

# ------------------------ STUDENT CRUD ------------------------

def student_to_dict(student):
    return {
        "student_id": student.student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "middle_name": student.middle_name,
        "course": student.course,
        "yearlevel": student.yearlevel,
        "email": student.email,
        "phone": student.phone,
        "contactnumber": student.contactnumber,
        "address": student.address,
        "emergencycontactnumber": student.emergencycontactnumber,
        "emergencycontactname": student.emergencycontactname,
        "cardexpirydate": student.cardexpirydate,
        "birthdate": student.birthdate,
        "schoolyear": student.schoolyear,
        "college": student.college,
    }

@csrf_exempt
@jwt_required
def get_students(request, student_id=None):
    if request.method == "GET":
        if student_id:
            try:
                student = StudentData.objects.get(pk=student_id)
                logger.info(f"200 OK: Retrieved student {student_id}")
                return JsonResponse(student_to_dict(student))
            except StudentData.DoesNotExist:
                logger.warning(f"404 Not Found: Student {student_id} not found")
                return JsonResponse({"error": "Student not found"}, status=404)
        else:
            students = StudentData.objects.all()
            data = [student_to_dict(s) for s in students]
            logger.info("200 OK: Retrieved all students")
            return JsonResponse(data, safe=False)
    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
@jwt_required
def create_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            student = StudentData.objects.create(**data)
            logger.info(f"201 Created: Student created with ID {student.student_id}")
            return JsonResponse(student_to_dict(student), status=201)
        except Exception as e:
            logger.error(f"400 Bad Request: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
@jwt_required
def update_student(request, student_id):
    if request.method == "PUT":
        try:
            student = StudentData.objects.get(pk=student_id)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(student, key, value)
            student.save()
            logger.info(f"200 OK: Student {student_id} updated")
            return JsonResponse(student_to_dict(student))
        except StudentData.DoesNotExist:
            logger.warning(f"404 Not Found: Student {student_id} not found for update")
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            logger.error(f"400 Bad Request: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['PUT'])

@csrf_exempt
@jwt_required
def patch_student(request, student_id):
    if request.method == "PATCH":
        try:
            student = StudentData.objects.get(pk=student_id)
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            student.save()
            logger.info(f"200 OK: Student {student_id} partially updated")
            return JsonResponse(student_to_dict(student))
        except StudentData.DoesNotExist:
            logger.warning(f"404 Not Found: Student {student_id} not found for patch")
            return JsonResponse({"error": "Student not found"}, status=404)
        except Exception as e:
            logger.error(f"400 Bad Request: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['PATCH'])

@csrf_exempt
@jwt_required
def delete_student(request, student_id):
    if request.method == "DELETE":
        try:
            student = StudentData.objects.get(pk=student_id)
            student.delete()
            logger.info(f"200 OK: Student {student_id} deleted")
            return JsonResponse({"message": "Student deleted successfully"})
        except StudentData.DoesNotExist:
            logger.warning(f"404 Not Found: Student {student_id} not found for deletion")
            return JsonResponse({"error": "Student not found"}, status=404)
    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['DELETE'])

# ------------------------ JWT USER AND TOKEN ------------------------

@api_view(['POST'])
def create_user_and_token(request):
    username = request.data.get('username', 'testuser')
    password = request.data.get('password', 'testpass123')

    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.save()
        logger.info(f"201 Created: User '{username}' created")
    else:
        logger.info(f"200 OK: Existing user '{username}' retrieved")

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return Response({
        "access_token": access_token,
        "refresh_token": str(refresh),
        "user_id": user.id,
        "username": user.username,
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

@api_view(['POST'])
def decode_jwt_token(request):
    token = request.data.get('token')
    if not token or not isinstance(token, str):
        return Response({"error": "Expected a string value"}, status=400)

    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        logger.info("200 OK: Token successfully decoded")
        return Response(decoded)
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token expired"}, status=401)
    except jwt.InvalidTokenError as e:
        return Response({"error": str(e)}, status=400)

