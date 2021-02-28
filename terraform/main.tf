terraform {
    required_providers {
        digitalocean = {
            source = "digitalocean/digitalocean"
            version = ">1.22.2"
        }
    }

    backend "remote" {
        organization = "ed-personal"

        workspaces {
            name = "spreadsheet-api-python"
        }
    }
}

provider "digitalocean" {
    token = var.do_token
}
