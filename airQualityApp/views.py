from django.shortcuts import render
from django.shortcuts import redirect
from airQualityApp.models import User, Device, Data
from airQualityApp.form import UserForm, DeviceForm
from airQualityApp.respone import Response_data
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from datetime import datetime

# Create your views here.

apiUrlHome = 'http://192.168.2.23:8001/api'
apiUrlSchool = 'http://192.168.20.139:8001/api'
apiUrlSchoolSever = 'http://192.168.20.111:8001/api'

api = apiUrlHome


def no_found(request):
    return render(request, 'no_found.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def data(request):
    users = User.objects.all()
    devices = Device.objects.all()
    data = Data.objects.all()
    return render(request, 'data.html', {
        'users': users,
        'devices': devices,
        'data': data
    })


def dashboard_view(request):
    users = User.objects.all()
    devices = Device.objects.all()
    data = Data.objects.all()
    return render(request, 'dashboard.html', {
        'users': users,
        'devices': devices,
        'data': data
    })


def get_devices_by_user(request, User_id):
    devices = Device.objects.filter(User_id=User_id)
    devices_data = [{'id': device.id, 'name': device.name} for device in devices]
    return JsonResponse(devices_data, safe=False)


def get_data_by_device(request, device_name_id):
    data = Data.objects.filter(device_name_id=device_name_id)
    data_info = [
        {
            'quantityCO2': d.quantityCO2,
            'quantityCO': d.quantityCO,
            'quantityNO2': d.quantityNO2,
            'quantityO3': d.quantityO3,
            'fine_particle': d.fine_particle,
            'temperature': d.temperature,
            'created_at': d.created_at
        } for d in data]
    return JsonResponse(data_info, safe=False)


def get_last_data(request):
    user = request.user
    print(f"Request : {request.body}")
    print(f"DB user : {user}")
    db_name = get_database_for_user(user)
    print(f"DB name: {db_name}")
    # result = Data.objects.using(db_name).order_by('-created_at').first()
    result = Data.objects.using('jos_user').order_by('-created_at').first()

    if result is None:
        return JsonResponse({"error": "No data found"}, status=404)

    data_info = {
        'quantityCO2': result.quantityCO2,
        'quantityCO': result.quantityCO,
        'quantityNO2': result.quantityNO2,
        'quantityO3': result.quantityO3,
        'fine_particle': result.fine_particle,
        'temperature': result.temperature,
        'fan': result.fan,
        'created_at': result.created_at
    }
    return JsonResponse(data_info, safe=False)


def fetch_data_from_api():
    url = f"{api}/data/ten"
    try:
        response = requests.get(url, timeout=10)  # Timeout en cas de lenteur
        response.raise_for_status()  # Vérifie les erreurs HTTP

        return response.json()  # Renvoie les données JSON
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return {"error": "Impossible de récupérer les données"}


def chart_data_gaz(request):
    api_data = fetch_data_from_api()

    # Vérification des données
    if "error" in api_data:
        return JsonResponse({"error": "Impossible de récupérer les données depuis l'API distante"}, status=500)

    # Transformation des données pour Chart.js
    labels = [
        datetime.fromisoformat(entry['created_at'].replace("Z", "")).strftime("%H:%M:%S")
        for entry in api_data
    ]
    co2_values = [entry['quantityCO2'] for entry in api_data]  # Données CO2
    co_values = [entry['quantityCO'] for entry in api_data]  # Données CO
    no2_values = [entry['quantityNO2'] for entry in api_data]  # Données NO2

    # Formatage des données pour Chart.js
    data = {
        "labels": labels,
        "datasets": [
            {
                "label": "CO2",
                "data": co2_values,
                "backgroundColor": "rgba(75, 192, 192, 0.7)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            },
            {
                "label": "CO",
                "data": co_values,
                "backgroundColor": "rgba(198, 173, 248, 0.7)",
                "borderColor": "rgba(198, 173, 248, 1)",
                "borderWidth": 1,
            },
            {
                "label": "NO2",
                "data": no2_values,
                "backgroundColor": "rgba(54, 162, 235, 0.7)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1,
            }
        ]
    }
    return JsonResponse(data)


def chart_fine_particle(request):
    api_data = fetch_data_from_api()

    # Vérification des données
    if "error" in api_data:
        return JsonResponse({"error": "Impossible de récupérer les données depuis l'API distante"}, status=500)

    # Transformation des données pour Chart.js
    labels = [
        datetime.fromisoformat(entry['created_at'].replace("Z", "")).strftime("%H:%M:%S")
        for entry in api_data
    ]
    fine_particle_values = [entry['fine_particle'] for entry in api_data]
    temperature_values = [entry['temperature'] for entry in api_data]

    # Formatage des données pour Chart.js
    data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Fine Particle",
                "data": fine_particle_values,
                "backgroundColor": "rgba(7, 69, 98, 0.7)",
                "borderColor": "rgba(7, 69, 98, 1)",
                "borderWidth": 1,
            },
            {
                "label": "Temperature",
                "data": temperature_values,
                "backgroundColor": "rgba(255, 225, 154, 0.7)",
                "borderColor": "rgba(255, 115, 114, 1)",
                "borderWidth": 1,
            }
        ]
    }
    return JsonResponse(data)


def chart_view(request):
    return render(request, 'chart.html')


def get_database_for_user(user):
    if user.username == 'user1':
        return 'default'
    elif user.username == 'user2':
        return 'user2_db'
    return 'default'
