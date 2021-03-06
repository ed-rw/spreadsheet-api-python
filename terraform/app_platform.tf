resource "digitalocean_app" "spreadsheet_api_python" {
  spec {
    name   = "spreadsheet-api-python"
    region = "nyc"

    service {
      name               = "spreadsheetapi"
      instance_count     = 1
      instance_size_slug = "basic-xxs"

      github {
        branch         = "master"
        deploy_on_push = false
        repo           = "ed-rw/spreadsheet-api-python"
      }

      dockerfile_path = "src/spreadsheetapi/Dockerfile"
      source_dir      = "src/spreadsheetapi"

      env {
        key   = "BACKEND"
        value = "InMemory"
        type  = "GENERAL"
      }

      health_check {
        http_path             = "/status"
        initial_delay_seconds = 4
        period_seconds        = 5
        timeout_seconds       = 3
        success_threshold     = 1
        failure_threshold     = 5
      }
    }
  }
}
