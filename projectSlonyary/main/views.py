from django.shortcuts import render, redirect, get_object_or_404
from .models import Users
from django.http import HttpResponse
from .models import InternshipModel
import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout


# ОБЩИЕ СТРАНИЦЫ
@csrf_exempt
def auth(request):
    if request.method == 'POST':
        user_login = request.POST.get('login')
        password = request.POST.get('password')
        role = 'редактор' if request.POST.get('role') == 'editor' else 'стажёр'

        user = Users.objects.filter(user_mail=user_login, user_password=password, user_function=role).first()

        if user:
            if role == 'редактор':
                request.session['user_id'] = user.user_id
                return redirect('index')
            elif role == 'стажёр':
                request.session['user_id'] = user.user_id
                return redirect('index1')
        else:
            return render(request, 'main/auth.html', {'error_message': 'Неверные данные для входа'})

    return render(request, 'main/auth.html')


@csrf_exempt
def registration(request):
    if request.method == "POST":
        user_mail = request.POST['email']
        user_login = request.POST['login']
        user_password = request.POST['password']

        user_function = request.POST.get('role')

        if request.POST['password'] == request.POST['password-confirm-field']:
            user = Users(
                user_mail=user_mail,
                user_login=user_login,
                user_password=user_password,
                user_function=user_function
            )
            user.save()
            return redirect('auth')
        else:
            return HttpResponse("Пароли не совпадают")

    return render(request, 'main/reg.html')


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('auth')


# СТРАНИЦЫ РЕДАКТОРА
@csrf_exempt
def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('auth')
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return HttpResponse("Ошибка: Пользователь не найден")

    if request.method == 'POST':
        user.user_firstname = request.POST.get('firstname', user.user_firstname)
        user.user_lastname = request.POST.get('lastname', user.user_lastname)
        user.save()

    context = {
        'firstname': user.user_firstname,
        'lastname': user.user_lastname,
        'email': user.user_mail,
        'user_role': user.user_function,
    }

    return render(request, 'main/profile.html', context)


@csrf_exempt
def index(request):
    return render(request, 'main/index.html')


@csrf_exempt
def constructor(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        photo = request.FILES.get('photo-select')
        start_date_raw = request.POST.get('start-date')
        end_date_raw = request.POST.get('end-date')
        address = request.POST.get('adress')
        contact = request.POST.get('contact')
        additional_info = request.POST.get('additional')

        try:
            start_date = datetime.datetime.strptime(start_date_raw, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_raw, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Некорректный формат дат. Укажите дату в формате ГГГГ-ММ-ДД")

        internship_row = InternshipModel(
            name=name,
            description=description,
            photo=photo,
            start_date=start_date,
            end_date=end_date,
            address=address,
            contact=contact,
            additional_info=additional_info
        )
        internship_row.save()

        messages.success(request, f"Стажировка '{name}' успешно создана!")

        return redirect('index')

    return render(request, 'main/constructor.html')


@csrf_exempt
def drafts(request):
    internships = InternshipModel.objects.all()

    context = {
        'internships': internships
    }
    return render(request, 'main/drafts.html', context)


@csrf_exempt
def edit_internship(request, id):
    try:
        internship_row = InternshipModel.objects.get(id=id)
    except InternshipModel.DoesNotExist:
        return HttpResponse("Стажировка не найдена")

    if request.method == 'POST':
        internship_row.name = request.POST.get('name', internship_row.name)
        internship_row.description = request.POST.get('description', internship_row.description)
        internship_row.address = request.POST.get('address', internship_row.address)
        internship_row.contact = request.POST.get('contact', internship_row.contact)
        internship_row.additional_info = request.POST.get('additional_info', internship_row.additional_info)

        if 'photo' in request.FILES:
            internship_row.photo = request.FILES['photo']
        internship_row.save()
        return redirect('drafts')

    context = {
        'internship': internship_row
    }
    return render(request, 'main/edit_internship.html', context)


# СТРАНИЦЫ СТАЖЁРА
@csrf_exempt
def profile1(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('auth')
    try:
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return HttpResponse("Ошибка: Пользователь не найден")

    if request.method == 'POST':
        user.user_firstname = request.POST.get('firstname', user.user_firstname)
        user.user_lastname = request.POST.get('lastname', user.user_lastname)
        user.save()

    context = {
        'firstname': user.user_firstname,
        'lastname': user.user_lastname,
        'email': user.user_mail,
        'user_role': user.user_function,
    }
    return render(request, 'main/profile1.html', context)


@csrf_exempt
def index1(request):
    return render(request, 'main/index1.html')


@csrf_exempt
def cards(request):
    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return HttpResponse("Пользователь не найден", status=404)

    internships = user.internship.all()

    context = {
        'internships': internships,
    }
    return render(request, 'main/cards.html', context)


@csrf_exempt
def internships_list(request):
    internships = InternshipModel.objects.all()
    return render(request, 'main/internships_list.html', {'internships': internships})


@csrf_exempt
def internship(request, id):
    try:
        internship_row = InternshipModel.objects.get(id=id)
    except InternshipModel.DoesNotExist:
        return HttpResponse("Стажировка не найдена", status=404)

    try:
        user_id = request.session.get('user_id')
        user = Users.objects.get(user_id=user_id)
    except Users.DoesNotExist:
        return HttpResponse(f"Пользователь не найден", status=404)

    if request.method == "POST":
        if user.internship.filter(id=internship_row.id).exists():
            messages.warning(request, "Вы уже записаны на эту стажировку.")
        else:
            user.internship.add(internship_row)
            messages.success(
                request,
                "Ваша форма принята, ожидайте ответа работодателя."
            )

    context = {
        'internship': internship_row
    }
    return render(request, 'main/internship.html', context)


@csrf_exempt
def card(request, id):
    try:
        internship = get_object_or_404(InternshipModel, id=id)

        context = {
            'internship': internship,
        }
        return render(request, 'main/card.html', context)
    except InternshipModel.DoesNotExist:
        return HttpResponse("Стажировка не найдена", status=404)



