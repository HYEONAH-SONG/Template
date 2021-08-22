# 세번째 개발 : 로직을 설계
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import TemplateSerializer
from .models import Template
import os, sys,shutil
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
import json


# Manage All Objects
class TemplateView(APIView):
	parser_classes = (MultiPartParser, FormParser)
		
	# upload template file
	def post(self, request, *args, **kwargs):
		serializer =TemplateSerializer(data=request.data)        
		if serializer.is_valid():                             	
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    # delete all templates 
	def delete(self,request):
		templates = Template.objects.all()
		shutil.rmtree('./media/')
		templates.delete()
		return Response("Delete All Templates Suceess!")
    
    # show all template information
	def get(self,request):
		templates = Template.objects.all()
		serializer =TemplateSerializer(templates,many=True)
		response = Response({"X-total-count":len(serializer.data),"list":serializer.data})
		response['Access-control-expose-headers'] =len(serializer.data) 
		if templates:
			return response
		else:
			return Response("There is no Template File")
	
# Manage Specific Object 
class TemplateDetails(APIView):
	def get_object(self, name):
		try:
			return Template.objects.get(name=name)
		except Template.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
	
	# show template content
	def get(self, request, name):
		templates = self.get_object(name)
		serializer = TemplateSerializer(templates)
		if 'json' in serializer.data['upload_files']:
			with open('.'+ serializer.data['upload_files'],"r") as f:
				content = json.load(f)
			#print(json.dumps(content,indent='\t'))		
			return Response(content)
		else:
			return Response("Invalid File")

	# delete template information
	def delete(self, request, name):
		templates = self.get_object(name)
		os.remove('.'+serializer.data['upload_files'])
		templates.delete()
		return Response("Delete Template File",status=status.HTTP_204_NO_CONTENT)

	# conversion JSON template file  --> file change
	def put(self, request, name):
		templates = self.get_object(name)
		serializer = TemplateSerializer(templates)

		cloudstack_instance = dict([("name","server-1"),("service_offering","Small Instance"),("network_id","6eb22f91-7454-4107-89f4-36afcdf33021"),("zone","zone1"),("template","centos 7")])
		openstack_instance = dict([("name","server-1"),("image_id","ad091b52-742f-469e-8f3c-fd81cadf0743"),("network",dict([("name","my_network")])),("flavor_name","m1.small")])
		cloudstack_volume = dict([("name","volume_1"),("size",3),("zone","zone-1")])
		openstack_volume = dict([("name","volume_1"),("region","RegionOne"),("size",3)])
		cloudstack_network = dict([("name","network_1"),("cidr","10.0.0.0/16"),("network_offering","Default Network"),("zone","zone-1")])
		openstack_network = dict([("name","network_1"),("admin_state_up","true")])
		# cloudstack_volume

		# before template file read	
		with open('.'+ serializer.data['upload_files'],'r') as json_file:
			json_data = json.load(json_file) # json -> dict
			type_ = json_data["resource"]

			if "openstack_compute_instance_v2" in type_: # openstack --> cloudstack
				type_["cloudstack_instance"] = type_.pop("openstack_compute_instance_v2")
				type_["cloudstack_instance"]["instance_1"] = cloudstack_instance
				print(json.dumps(type_, indent='\t'))

			elif "cloudstack_instance" in type_: # cloudstack --> openstack
				type_["openstack_compute_instance_v2"] = type_.pop("cloudstack_instance")
				type_["openstack_compute_instance_v2"]["instance_1"] = openstack_instance
				print(json.dumps(type_, indent='\t'))

			elif "openstack_blockstorage_volume_v3" in type_: # cloudstack --> openstack
				type_["cloudstack_disk"] = type_.pop("openstack_blockstorage_volume_v3")
				type_["cloudstack_disk"]["volume_1"] = cloudstack_volume
				print(json.dumps(type_, indent='\t'))

			elif "cloudstack_disk" in type_: # cloudstack --> openstack
				type_["openstack_blockstorage_volume_v3"] = type_.pop("cloudstack_disk")
				type_["openstack_blockstorage_volume_v3"]["volume_1"] = openstack_volume
				print(json.dumps(type_, indent='\t'))

			elif "openstack_networking_network_v2" in type_: # openstack --> cloudstack
				type_["cloudstack_network"] = type_.pop("cloudstack_disk")
				type_["cloudstack_network"]["network_1"] = openstack_volume
				print(json.dumps(type_, indent='\t'))	
					
			elif "cloudstack_network" in type_: # cloudstack --> openstack
				type_["openstack_networking_network_v2"] = type_.pop("cloudstack_network")
				type_["openstack_networking_network_v2"]["network_1"] = openstack_volume
				print(json.dumps(type_, indent='\t'))

		# write template file after conversing
		with open('.'+ serializer.data['upload_files'], "w", encoding="utf-8") as mk_f:
			json.dump(json_data, mk_f, indent='\t')

		# read after conversing template file
		with open('.'+ serializer.data['upload_files'], "r", encoding="utf-8") as f:
			json_data = json.load(f)
		print(json.dumps(json_data, indent='\t'))
		return Response(json_data)

class Terraform(APIView):
	def get_object(self, name):
		try:
			return Template.objects.get(name=name)
		except Template.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)	

	# terraform apply
	def get(self,request,name):
		templates = self.get_object(name)
		serializer = TemplateSerializer(templates)
		# read file 
		with open('.'+ serializer.data['upload_files'],"r") as f:
			json_data = json.load(f)
		# write file to main.tf
		with open('./terraform/main.tf.json', "w", encoding="utf-8") as mk_f:
			json.dump(json_data, mk_f, indent='\t')
		os.chdir("./terraform/") # terraform 으로 현재 디렉토리 변경
		os.system('terraform init')
		os.system('terraform plan')
		os.system('terraform apply')
		return Response("terraform apply success",status = status.HTTP_201_CREATED)

class Terraform_Destroy(APIView):
	# terraform destroy
	def delete(self, request):
		os.chdir("C:/Users/송영진/Desktop/Template_Conversion/terraform/")
		os.system('terraform destroy')
		return Response("Destroy Success!")



