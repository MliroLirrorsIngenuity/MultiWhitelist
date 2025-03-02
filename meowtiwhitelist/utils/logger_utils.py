from mcdreforged.api.all import *

from meowtiwhitelist.utils.translater_utils import tr
from meowtiwhitelist.utils.uuid_utils.service_loader import api_services


def log(source: CommandSource,text):
    text = RTextList(text)
    source.get_server().broadcast(text)


def log_available_apis(src):
    log(src, tr("available_apis.header"))
    valid_services = [s for s in api_services if s.get('id', -1) > 0]

    if not valid_services:
        log(src, tr("available_apis.none"))
        return

    for service in valid_services:
        log(src, tr("available_apis.item",service['name'],service['id']))