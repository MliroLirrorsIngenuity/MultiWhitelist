import os

from mcdreforged.api.all import *

from meowtiwhitelist.constants import CONFIG_FILE, CONFIG_DIR


class Configuration(Serializable):
    server_dirname: str = "server"
    permission: int = 3

    def save(self) -> None:
        server_interface = ServerInterface.get_instance().as_plugin_server_interface()
        server_interface.save_config_simple(self, CONFIG_FILE, in_data_folder=False)

def load_configuration() -> Configuration:
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

    server_interface = ServerInterface.get_instance().as_plugin_server_interface()

    if not os.path.exists(CONFIG_FILE):
        _config = Configuration()
        _config.save()
    else:
        _config = server_interface.load_config_simple(
            CONFIG_FILE,
            target_class=Configuration,
            in_data_folder=False,
            source_to_reply=None,
        )
    return _config

config = load_configuration()
server_dirname = config.server_dirname