from django.shortcuts import render
import json
from .models import Account
from django.views import View
from django.http import HttpResponse, JsonResponse
# DB 테이블의 데이터를 처리하는 로직 생성

# 사용자 정보 저장, 회원가입
class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)
        Account.objects.create(
            name = data['name'],
            password = data['password']
        )
        return JsonResponse(data,status = 200)
    
    def get(self, request):
        Account_data = Account.objects.values()
        return JsonResponse({'accounts' : list(Account_data)}, status = 200)

    def delete(self,request):
        Account_data = Account.objects.all()
        Account_data.delete()
        return HttpResponse("Delete Success")


# 로그인
class SignView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(name = data['name']).exists():
                user = Account.objects.get(name=data['name'])
                if user.password == data['password']:
                    return HttpResponse("Success",status=200)
                return HttpResponse("Wrong Password",status=401)
            return HttpResponse("Invalid name",status = 400)

        except KeyError:
            return JsonResponse({'message': "INVALID_KEYS"}, status =400 )
