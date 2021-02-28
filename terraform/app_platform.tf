resource "digitalocean_app" "spreadsheet_api_python" {
  spec {
    name   = "spreadsheet-api-python"
    region = "nyc1"

    service {
      name           = "spreadsheetapi"
      instance_count = 1

      github {
        branch         = "master"
        deploy_on_push = false
        repo           = "ed-rw/spreadsheet-api-python"
      }

      dockerfile_path = "src/spreadsheetapi/Dockerfile"

      env {
        key   = "BACKEND"
        value = "InMemory"
        type  = "GENERAL"
      }
    }
  }
}
