from django.conf.urls import url
from .views import TemplateView, TemplateDetails, Terraform, Terraform_Destroy
from django.urls import path

urlpatterns = [
  	path('', TemplateView.as_view(), name='template_CRD'),
    path('<name>/', TemplateDetails.as_view()),
    path('terraform/<name>/', Terraform.as_view()),
    path('terraform/', Terraform_Destroy.as_view()),    
]