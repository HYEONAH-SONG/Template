# Cloudstack Provider
terraform {
  required_providers {
    cloudstack = {
      source = "orange-cloudfoundry/cloudstack"
      version = "0.4.0"
    }
    openstack = {
      source = "terraform-provider-openstack/openstack"
      version = "1.43.0"
    }
  }
}

provider "cloudstack" {
  api_url    = "http://164.125.70.26:8080/client/api"
  api_key    = "0OcHRmqlLKxseRjIRoqW2sBtpIbaDDvnUElpbZVedZIVoZ1F11fcKi1n1MDGNuDWDXxBnG6Ba-jMFqSpAi5Tfg"
  secret_key = "xtbZVaUeYuds-ke_lCyRh0pZSdKdzUNHufwJeSvynO6847jJpWEb_aODEvsuHZ10os--xVFRAl3jepBiA33BAA"
}

provider "openstack" {
  user_name   = "admin"
  tenant_name = "admin"
  password    = "0000"
  auth_url    = "http://164.125.70.22/identity/"
  region      = "RegionOne"
}

