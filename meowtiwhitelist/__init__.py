from mcdreforged.api.all import *

from meowtiwhitelist.constants import PREFIX
from meowtiwhitelist.utils.file_utils import create_example_files
from meowtiwhitelist.utils.translater_utils import tr
from meowtiwhitelist.command import register_command


def on_load(server: PluginServerInterface, prev):
    server.register_help_message(PREFIX, tr("help_msg_name"))
    create_example_files()
    register_command(server)