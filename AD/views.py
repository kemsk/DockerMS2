import json
import jwt
import logging
from django.http import JsonResponse, HttpResponseNotAllowed
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from AD.permissions import IsAdmin, IsPersonnel
from .models import User
from rest_framework import status
from .models import StudentData
from .models import AdminData
from .serializers import PhotoUploadSerializer , StudentSerializer
from django.utils.datastructures import MultiValueDictKeyError
from .models import PhotoUpload
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q


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
    photos = student.photos.all()  # using related_name='photos' from your model
    photo_list = [
        {
            "id": photo.id,
            "title": photo.title,
            "image_url": f"{settings.MEDIA_URL}{photo.image.name}",
            "uploaded_at": photo.uploaded_at.isoformat()
        }
        for photo in photos
    ]
    
    return {
        "id": student.student_id, 
        "student_id": student.student_id,
        "last_name": student.last_name,
        "first_name": student.first_name,
        "middle_name": student.middle_name,
        "course": student.course,
        "year_level": student.year_level,
        "email": student.email,
        "address": student.address,
        "phone_number": student.phone_number,
        "emergency_contact_number": student.emergency_contact_number,
        "emergency_contact_name": student.emergency_contact_name,
        "card_expiry_date": student.card_expiry_date,
        "birthdate": student.birthdate,
        "school_year": student.school_year,
        "college": student.college,
        "student_photos": photo_list  # now includes uploaded photos
    }

@api_view(['GET'])
@permission_classes([IsPersonnel])
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
            query = request.GET.get('q')
            if query:
                students = StudentData.objects.filter(first_name__icontains=query)[:10]
            else:
                students = StudentData.objects.all()
            data = [student_to_dict(s) for s in students]
            logger.info("200 OK: Retrieved student list")
            return JsonResponse(data, safe=False)
    
    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['GET'])

@api_view(['GET'])
@permission_classes([IsPersonnel])
def student_suggestions(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return Response([], status=status.HTTP_200_OK)

    students = StudentData.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query)
    )[:10]  # Limit to 10 results

    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# ------------------------ CREATE STUDENT ------------------------>>
@api_view(['POST'])
@permission_classes([IsAdmin]) 
def create_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            valid_fields = {
                "student_id",
                "last_name",
                "first_name",
                "middle_name",
                "course",
                "year_level",
                "email",
                "address",
                "phone_number",
                "emergency_contact_number",
                "emergency_contact_name",
                "card_expiry_date",
                "birthdate",
                "school_year",
                "college"
            }

            filtered_data = {key: value for key, value in data.items() if key in valid_fields}

            student = StudentData.objects.create(**filtered_data)
            logger.info(f"201 Created: Student created with ID {student.student_id}")
            return JsonResponse(student_to_dict(student), status=201)

        except Exception as e:
            logger.error(f"400 Bad Request: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)

    logger.warning("405 Method Not Allowed")
    return HttpResponseNotAllowed(['POST'])




@api_view(['PUT' ,'PATCH', 'DELETE'])
@permission_classes([IsAdmin]) 
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

@permission_classes([IsAdmin]) 
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

@permission_classes([IsAdmin])
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

# ------------------------ JWT USER AND TOKEN ------------------------#



@api_view(['POST'])
@permission_classes([IsAdmin]) 
def create_user(request):
    # Only allow admins to create new users
    
    if not request.user or not request.user.is_staff:
        return Response({"error": "Permission denied. Only admins can create users."}, status=403)

    # Extract data from the request
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    role = request.data.get('role')  # The role field: "admin" or "personnel"

    # Validate required fields
    if not username or not password or not email or not role:
        return Response({"error": "Username, password, email, and role are required."}, status=400)

    # Validate role
    if role not in ["admin", "personnel"]:
        return Response({"error": "Invalid role. Allowed values are 'admin' or 'personnel'."}, status=400)

    # Prevent duplicate email
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists."}, status=400)

    # Prevent duplicate username
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=400)

    # Create user
    is_staff = role == "admin"  # Admins have is_staff=True
    user = User.objects.create_user(username=username, email=email, password=password, is_staff=is_staff)
    
    logger.info(f"201 Created: User '{username}' with role '{role}' created")

    return Response({
        "user_id": user.id,
        "username": user.username,
        "role": role,
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Validate the data
    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return JsonResponse({
            "access_token": access_token,
            "refresh_token": str(refresh),
            "user_id": user.id,
            "username": user.username,
            "role": "admin" if user.is_staff else "personnel",
        }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

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

#ADMIN CRUD

def admin_to_dict(admin):
    return {
        "admin_id": admin.admin_id,
        "first_name": admin.first_name,
        "middle_name": admin.middle_name,
        "last_name": admin.last_name,
        "email": admin.email,
        "phone_number": admin.phone_number,
        "address": admin.address,
        "emergency_contactname": admin.emergency_contactname,
        "emergency_contact_number": admin.emergency_contact_number,
        "card_expiry_date": admin.card_expiry_date,
    }

@api_view(['GET'])
@permission_classes([IsAdmin])
def get_admins(request, admin_id=None):
    if request.method == "GET":
        if admin_id:
            try:
                admin = AdminData.objects.get(pk=admin_id)
                return JsonResponse(admin_to_dict(admin))
            except AdminData.DoesNotExist:
                return JsonResponse({"error": "Admin not found"}, status=404)
        else:
            admins = AdminData.objects.all()
            return JsonResponse([admin_to_dict(a) for a in admins], safe=False)
    return HttpResponseNotAllowed(['GET'])


@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_admin(request, admin_id):
    if request.method == "PUT":
        try:
            admin = AdminData.objects.get(pk=admin_id)
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(admin, key, value)
            admin.save()
            return JsonResponse(admin_to_dict(admin))
        except AdminData.DoesNotExist:
            return JsonResponse({"error": "Admin not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseNotAllowed(['PUT'])


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def patch_admin(request, admin_id):
    if request.method == "PATCH":
        try:
            admin = AdminData.objects.get(pk=admin_id)
            data = json.loads(request.body)
            for key, value in data.items():
                if hasattr(admin, key):
                    setattr(admin, key, value)
            admin.save()
            return JsonResponse(admin_to_dict(admin))
        except AdminData.DoesNotExist:
            return JsonResponse({"error": "Admin not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseNotAllowed(['PATCH'])


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_admin(request, admin_id):
    if request.method == "DELETE":
        try:
            admin = AdminData.objects.get(pk=admin_id)
            admin.delete()
            return JsonResponse({"message": "Admin deleted successfully"})
        except AdminData.DoesNotExist:
            return JsonResponse({"error": "Admin not found"}, status=404)
    return HttpResponseNotAllowed(['DELETE'])


@api_view(['POST'])
@permission_classes([IsPersonnel])
def upload_photo(request):
    if request.method == "POST":
        try:
            student_id = request.POST['student']
            student = StudentData.objects.get(pk=student_id)
        except MultiValueDictKeyError:
            return JsonResponse({'error': 'Student ID is required.'}, status=400)
        except StudentData.DoesNotExist:
            return JsonResponse({'error': 'Student not found.'}, status=404)

        # Corrected serializer call
        data = request.POST.copy()
        data['image'] = request.FILES.get('image')
        serializer = PhotoUploadSerializer(data=data)

        if serializer.is_valid():
            serializer.save(student=student)  # overrides posted `student` field
            return JsonResponse(serializer.data, status=201)
        return JsonResponse({'error': 'Invalid image upload', 'details': serializer.errors}, status=400)

    return HttpResponseNotAllowed(['POST'])


@api_view(['GET'])
@permission_classes([IsPersonnel])
def get_photos_by_student(request, student_id):
    if request.method == "GET":
        try:
            student = StudentData.objects.get(pk=student_id)
            photos = PhotoUpload.objects.filter(student=student)
            serializer = PhotoUploadSerializer(photos, many=True)
            return JsonResponse(serializer.data, safe=False)
        except StudentData.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)
    return HttpResponseNotAllowed(['GET'])


