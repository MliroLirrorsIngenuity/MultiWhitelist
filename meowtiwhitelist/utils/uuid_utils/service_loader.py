import os
import yaml
from meowtiwhitelist.constants import SERVICE_DIR

def load_all_services():
    if not os.path.exists(SERVICE_DIR):
        os.makedirs(SERVICE_DIR, exist_ok=True)

    api_configs = []
    for filename in os.listdir(SERVICE_DIR):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            file_path = os.path.join(SERVICE_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                config["id"] = int(config["id"])
                api_configs.append(config)

    return api_configs


api_services = load_all_services()


def build_service_mapping() -> dict:
    service_map = {}
    for service in api_services:
        if (service_id := service.get('id', -1)) <= 0:
            continue

        normalized_name = service.get('name', '').strip().lower()
        service_map.update({
            normalized_name: service_id,
            str(service_id): service_id
        })
    return service_map