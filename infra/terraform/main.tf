terraform {
  required_version = ">= 1.6"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
  }
}
variable "subscription_id" { type = string }
variable "location" { type = string, default = "northeurope" }
variable "storage_name" { type = string }
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
resource "azurerm_resource_group" "health" {
  name = "healthcare-multimodal-demo-rg"
  location = var.location
}
resource "azurerm_storage_account" "health" {
  name = var.storage_name
  resource_group_name = azurerm_resource_group.health.name
  location = azurerm_resource_group.health.location
  account_tier = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled = true
  min_tls_version = "TLS1_2"
  allow_nested_items_to_be_public = false
}
resource "azurerm_storage_data_lake_gen2_filesystem" "research" {
  name = "research"
  storage_account_id = azurerm_storage_account.health.id
}
