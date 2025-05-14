from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ClientAuthenticationError

# 🔹 Authenticate using DefaultAzureCredential (supports MSI & Service Principal)
try:
    credential = DefaultAzureCredential()
    print("✅ Authentication successful!")
except ClientAuthenticationError as e:
    print(f"❌ Authentication failed: {e}")
    exit(1)

# 🔹 Set subscription ID
SUBSCRIPTION_ID = ""  # Fill this manually or fetch dynamically

if not SUBSCRIPTION_ID:
    SUBSCRIPTION_ID = input("Enter Azure Subscription ID: ").strip()

compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

def get_vm_resource_group(vm_name):
    """Fetches the resource group of a VM dynamically if not provided."""
    try:
        for vm in compute_client.virtual_machines.list_all():
            if vm.name.lower() == vm_name.lower():
                return vm.id.split("/")[4]  # Extracts resource group name from VM ID
    except Exception as e:
        print(f"❌ Error fetching VM resource group: {e}")
    return None

def start_vm(resource_group, vm_name):
    """Starts an Azure Virtual Machine."""
    try:
        print(f"🚀 Starting VM: {vm_name} in Resource Group: {resource_group}...")
        compute_client.virtual_machines.begin_start(resource_group, vm_name).result()
        print("✅ VM started successfully!")
    except Exception as e:
        print(f"❌ Error starting VM: {e}")

def stop_vm(resource_group, vm_name):
    """Stops an Azure Virtual Machine."""
    try:
        print(f"🛑 Stopping VM: {vm_name} in Resource Group: {resource_group}...")
        compute_client.virtual_machines.begin_power_off(resource_group, vm_name).result()
        print("✅ VM stopped successfully!")
    except Exception as e:
        print(f"❌ Error stopping VM: {e}")

def restart_vm(resource_group, vm_name):
    """Restarts an Azure Virtual Machine."""
    try:
        print(f"🔄 Restarting VM: {vm_name} in Resource Group: {resource_group}...")
        compute_client.virtual_machines.begin_restart(resource_group, vm_name).result()
        print("✅ VM restarted successfully!")
    except Exception as e:
        print(f"❌ Error restarting VM: {e}")

if __name__ == "__main__":
    vm_name = input("Enter VM Name: ").strip()

    # Optional input for resource group
    resource_group = input("Enter Resource Group (press Enter to auto-detect): ").strip() or get_vm_resource_group(vm_name)

    if not resource_group:
        print("❌ Resource Group not found for the given VM name!")
        exit(1)

    action = input("Enter action (start/stop/restart): ").strip().lower()

    if action == "start":
        start_vm(resource_group, vm_name)
    elif action == "stop":
        stop_vm(resource_group, vm_name)
    elif action == "restart":
        restart_vm(resource_group, vm_name)
    else:
        print("❌ Invalid action. Choose from: start, stop, restart.")
