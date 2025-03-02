from mcdreforged.api.all import *

from meowtiwhitelist.constants import PREFIX
from meowtiwhitelist.utils.config_utils import config
from meowtiwhitelist.utils.logger_utils import log, log_available_apis
from meowtiwhitelist.utils.translater_utils import tr
from meowtiwhitelist.operations import add_whitelist, remove_whitelist, list_whitelist


def register_command(server: PluginServerInterface):
    def get_literal_node(literal):
        return Literal(literal)

    def show_help(src: CommandSource):
        log(src, tr("help_msg", PREFIX))
        log_available_apis(src)

    server.register_command(
        Literal(PREFIX)
        .requires(lambda src: src.has_permission(config.permission))
        .on_error(
            RequirementNotMet,
            lambda src: log(src, tr("error.permission_denied")),
            handled=True,
        )
        .runs(lambda src: show_help(src))
        .then(
            get_literal_node("help")
            .runs(lambda src: show_help(src))
        )
        .then(
            get_literal_node("add")
            .runs(lambda src: log(src, tr("error.add_require_name", PREFIX)))
            .then(
                Text("player_name").runs(lambda src: log(src, tr("error.require_api", PREFIX)))
                .then(
                    Text("api").runs(lambda src, ctx: add_whitelist(src, ctx["player_name"], ctx["api"]))
                    .on_error(
                        RequirementNotMet,
                        lambda src, ctx: log(src, tr("error.unknown_error", ctx["player_name"])),
                        handled=True,
                    )
                )
            )
        )
        .then(
            get_literal_node("remove")
            .runs(lambda src: log(src, tr("error.remove_require_name", PREFIX)))
            .then(
                Text("player_name").runs(lambda src, ctx: remove_whitelist(src, ctx["player_name"]))
            )
        )
        .then(
            get_literal_node("list")
            .runs(lambda src: list_whitelist(src))
        )
    )