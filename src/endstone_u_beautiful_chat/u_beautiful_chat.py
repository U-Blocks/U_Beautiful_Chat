import os
import json
import datetime

from endstone import ColorFormat, Player
from endstone.plugin import Plugin
from endstone.command import Command, CommandSender, CommandSenderWrapper
from endstone.form import ActionForm, ModalForm, TextInput, Dropdown, Toggle
from endstone.event import event_handler, PlayerChatEvent, PlayerJoinEvent, PlayerQuitEvent

from endstone_u_beautiful_chat.lang import load_lang_data

current_dir = os.getcwd()

first_dir = os.path.join(current_dir, "plugins", "u-beautiful-chat")

if not os.path.exists(first_dir):
    os.mkdir(first_dir)

nickname_data_file_path = os.path.join(first_dir, "nickname.json")

mute_data_file_path = os.path.join(first_dir, "mute.json")

config_data_file_path = os.path.join(first_dir, "config.json")

lang_dir = os.path.join(first_dir, "lang")

if not os.path.exists(lang_dir):
    os.mkdir(lang_dir)


class u_beautiful_chat(Plugin):
    api_version = "0.10"

    def __init__(self):
        super().__init__()

        # load data: nickname
        if not os.path.exists(nickname_data_file_path):
            with open(nickname_data_file_path, "w", encoding="utf-8") as f:
                nickname_data = {}
                json_str = json.dumps(nickname_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(nickname_data_file_path, "r", encoding="utf-8") as f:
                nickname_data = json.loads(f.read())

        self.nickname_data = nickname_data

        # load data: mute
        if not os.path.exists(mute_data_file_path):
            with open(mute_data_file_path, "w") as f:
                mute_data = []
                json_str = json.dumps(mute_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(mute_data_file_path, "r") as f:
                mute_data = json.loads(f.read())

        self.mute_data = mute_data

        # load data: config
        if not os.path.exists(config_data_file_path):
            with open(config_data_file_path, "w") as f:
                config_data = {
                    "variables_order": "",
                    "is_set_or_update_nickname_enabled": True,
                    "max_nickname_len": 10,
                    "set_or_update_nickname_cost": 10,
                    "is_record_history_message_enabled": True,
                    "max_history_message_num_recorded": 10,
                    "is_simplify_join_or_left_prompt_enabled": True
                }
                json_str = json.dumps(config_data, indent=4, ensure_ascii=False)
                f.write(json_str)
        else:
            with open(config_data_file_path, "r") as f:
                config_data = json.loads(f.read())

        self.config_data = config_data

        # load data: lang
        self.lang_data = load_lang_data(lang_dir)

        self.message_recorder = []

    def on_enable(self):
        is_ustatistic_installed = self.server.plugin_manager.get_plugin("ustatistic")

        is_umoney_installed = self.server.plugin_manager.get_plugin("umoney")

        if is_ustatistic_installed and is_umoney_installed:
            pass
        else:
            if not is_ustatistic_installed and is_umoney_installed:
                self.logger.error(
                    f"{ColorFormat.RED}"
                    f"Pre-plugin U-Statistic is required..."
                )
            elif is_ustatistic_installed and not is_umoney_installed:
                self.logger.error(
                    f"{ColorFormat.RED}"
                    f"Pre-plugin UMoney is required..."
                )
            else:
                self.logger.error(
                    f"{ColorFormat.RED}"
                    f"Pre-plugins U-Statistic and UMoney are required..."
                )

            self.server.plugin_manager.disable_plugin(self)

            return

        self.command_sender_wrapper = CommandSenderWrapper(
            sender=self.server.command_sender,
            on_message=None
        )

        self.register_events(self)

        self.logger.info(
            f"{ColorFormat.YELLOW}"
            f"U-Beautiful-Chat is enabled..."
        )

    commands = {
        "ubc": {
            "description": "Call out the main form of U-Beautiful-Chat",
            "usages": ["/ubc"],
            "permissions": ["u_beautiful_chat.command.ubc"]
        }
    }

    permissions = {
        "u_beautiful_chat.command.ubc": {
            "description": "Call out the main form of U-Beautiful-Chat",
            "default": True
        }
    }

    def on_command(self, sender: CommandSender, command: Command, args: list[str]):
        if command.name == "ubc":
            if not isinstance(sender, Player):
                sender.send_message(
                    f"{ColorFormat.RED}"
                    f"This command can only be executed by a player...."
                )

                return

            money = self.server.plugin_manager.get_plugin("umoney").api_get_player_money(sender.name)

            nickname = self.nickname_data[sender.name]["nickname"]

            unique_nickname = self.nickname_data[sender.name]["unique_nickname"]

            main_form = ActionForm(
                title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                      f"{self.get_text(sender, 'main_form.title')}",
                content=f"{ColorFormat.GREEN}"
                        f"{self.get_text(sender, 'money')}: "
                        f"{ColorFormat.WHITE}"
                        f"{money}\n"
                        f"{ColorFormat.GREEN}"
                        f"{self.get_text(sender, 'nickname')}: "
                        f"{ColorFormat.WHITE}"
                        f"{nickname}\n"
                        f"{ColorFormat.GREEN}"
                        f"{self.get_text(sender, "unique_nickname")}: "
                        f"{ColorFormat.WHITE}"
                        f"{unique_nickname}\n"
                        f"\n"
                        f"{ColorFormat.GREEN}"
                        f"{self.get_text(sender, 'main_form.content')}",
            )

            if self.config_data["is_set_or_update_nickname_enabled"]:
                main_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(sender, 'main_form.button.set_nickname')}",
                    icon="textures/ui/emptyStar",
                    on_click=self.set_nickname
                )

            if sender.is_op:
                main_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(sender, 'main_form.button.set_unique_nickname')}",
                    icon="textures/ui/filledStar",
                    on_click=self.set_unique_nickname
                )

                main_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(sender, 'main_form.button.muted_player')}",
                    icon="textures/ui/mute_on",
                    on_click=self.muted_player
                )

                main_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(sender, 'main_form.button.reload_config')}",
                    icon="textures/ui/icon_setting",
                    on_click=self.reload_configuration
                )

            if self.server.plugin_manager.get_plugin("zx_ui"):
                main_form.on_close = self.back_to_zx_ui

                main_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(sender, 'button.back_to_zx_ui')}",
                    icon="textures/ui/refresh_light",
                    on_click=self.back_to_zx_ui
                )
            else:
                main_form.on_close = None

                main_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(sender, 'button.close')}",
                    icon="textures/ui/cancel",
                    on_click=None
                )

            sender.send_form(main_form)

    def set_nickname(self, player: Player):
        money = self.server.plugin_manager.get_plugin("umoney").api_get_player_money(player.name)

        nickname = self.nickname_data[player.name]["nickname"]

        textinput = TextInput(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'money')}: "
                  f"{ColorFormat.WHITE}"
                  f"{money}\n"
                  f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'nickname')}: "
                  f"{ColorFormat.WHITE}"
                  f"{nickname}\n"
                  f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'set_or_update_nickname_cost')}: "
                  f"{ColorFormat.WHITE}"
                  f"{self.config_data['set_or_update_nickname_cost']}\n"
                  f"\n"
                  f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'set_nickname_form.textinput.label')}",
            placeholder=self.get_text(player, "set_nickname_form.textinput.placeholder").format(self.config_data["max_nickname_len"])
        )

        if len(nickname) != 0:
            textinput.default_value = nickname

        set_nickname_form = ModalForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'set_nickname_form.title')}",
            controls=[textinput],
            submit_button=f"{ColorFormat.YELLOW}"
                          f"{self.get_text(player, 'set_nickname_form.submit_button')}",
            on_close=self.back_to_main_form
        )

        def on_submit(p: Player, json_str: str):
            data = json.loads(json_str)

            if len(data[0]) > self.config_data["max_nickname_len"]:
                p.send_message(
                    f"{ColorFormat.RED}"
                    f"{self.get_text(p, 'message.error')}"
                )

                return

            self.nickname_data[p.name]["nickname"] = data[0]

            self.save_nickname_data()

            p.send_message(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(p, 'set_nickname.message.success')}"
            )

            self.server.plugin_manager.get_plugin("umoney").api_change_player_money(p.name, -self.config_data["set_or_update_nickname_cost"])

        set_nickname_form.on_submit = on_submit

        player.send_form(set_nickname_form)

    def set_unique_nickname(self, player: Player):
        player_name_list = [key for key in self.nickname_data.keys()]

        player_name_list.sort(key=lambda x:x[0].lower(), reverse=False)

        dropdown = Dropdown(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'set_unique_nickname_form.dropdown')}",
            options=player_name_list,
            default_index=0
        )

        set_unique_nickname_form = ModalForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'set_unique_nickname_form.title')}",
            controls=[dropdown],
            submit_button=f"{ColorFormat.YELLOW}"
                          f"{self.get_text(player, 'set_unique_nickname_form.submit_button')}",
            on_close=self.back_to_main_form
        )

        def on_submit(p: Player, json_str: str):
            data = json.loads(json_str)

            target_player_name = player_name_list[data[0]]

            target_player_unique_nickname = self.nickname_data[target_player_name]["unique_nickname"]

            textinput = TextInput(
                label=f"{ColorFormat.GREEN}"
                      f"{self.get_text(p, 'set_unique_nickname_form1.textinput.label1').format(target_player_name)}\n"
                      f"\n"
                      f"{self.get_text(p, 'unique_nickname')}: "
                      f"{ColorFormat.WHITE}"
                      f"{target_player_unique_nickname}\n"
                      f"\n"
                      f"{ColorFormat.GREEN}"
                      f"{self.get_text(p, 'set_unique_nickname_form1.textinput.label2')}",
                placeholder=self.get_text(p, 'set_unique_nickname_form1.textinput.placeholder')
            )

            set_unique_nickname_form1 = ModalForm(
                title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                      f"{self.get_text(p, 'set_unique_nickname_form1.title')}",
                controls=[textinput],
                submit_button=f"{ColorFormat.YELLOW}"
                              f"{self.get_text(p, 'set_unique_nickname_form1.submit_button')}",
                on_close=self.set_unique_nickname
            )

            def on_submit1(p1: Player, json_str1: str):
                data1 = json.loads(json_str1)

                self.nickname_data[target_player_name]["unique_nickname"] = data1[0]

                self.save_nickname_data()

                p1.send_message(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(p1, 'set_unique_nickname.message.success').format(target_player_name)}"
                )

            set_unique_nickname_form1.on_submit = on_submit1

            p.send_form(set_unique_nickname_form1)

        set_unique_nickname_form.on_submit = on_submit

        player.send_form(set_unique_nickname_form)

    def muted_player(self, player: Player):
        muted_player_form = ActionForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'muted_player_form.title')}",
            content=f"{ColorFormat.GREEN}"
                    f"{self.get_text(player, 'muted_player_form.content')}",
            on_close=self.back_to_main_form
        )

        if player.is_op:
            muted_player_form.add_button(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, 'muted_player_form.button.mute_player')}",
                icon="textures/ui/mute_on",
                on_click=self.mute_player
            )

        for player_name in self.mute_data:
            muted_player_form.add_button(
                f"{ColorFormat.YELLOW}"
                f"{player_name}",
                icon="textures/ui/icon_steve",
                on_click=self.single_muted_player(player_name)
            )

        muted_player_form.add_button(
            f"{ColorFormat.YELLOW}"
            f"{self.get_text(player, 'button.back_to_previous')}",
            icon="textures/ui/refresh_light",
            on_click=self.back_to_main_form
        )

        player.send_form(muted_player_form)

    def mute_player(self, player: Player):
        player_name_list = []

        for key in self.nickname_data.keys():
            if key not in self.mute_data and key != player.name:
                player_name_list.append(key)

        if len(player_name_list) == 0:
            player.send_message(
                f"{ColorFormat.RED}"
                f"{self.get_text(player, 'mute_player.message.fail')}"
            )

            return

        player_name_list.sort(key=lambda x:x[0].lower(), reverse=True)

        dropdown = Dropdown(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'mute_player_form.dropdown.label')}",
            options=player_name_list,
            default_index=0
        )

        mute_player_form = ModalForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'mute_player_form.title')}",
            controls=[dropdown],
            submit_button=f"{ColorFormat.YELLOW}"
                          f"{self.get_text(player, 'mute_player_form.submit_button')}",
            on_close=self.muted_player
        )

        def on_submit(p: Player, json_str: str):
            data = json.loads(json_str)

            player_to_mute_name = player_name_list[data[0]]

            self.mute_data.append(player_to_mute_name)

            self.save_mute_data()

            p.send_message(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(p, 'mute_player.message.success').format(player_to_mute_name)}"
            )

        mute_player_form.on_submit = on_submit

        player.send_form(mute_player_form)

    def single_muted_player(self, player_name: str):
        def on_click(player: Player):
            single_muted_player_form = ActionForm(
                title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                      f"{player_name}",
                content=f"{ColorFormat.GREEN}"
                        f"{self.get_text(player, 'single_muted_player_form.content')}",
                on_close=self.muted_player
            )

            single_muted_player_form.add_button(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, 'single_muted_player_form.button.unmute')}",
                icon="textures/ui/icon_unlocked",
                on_click=self.unmute_player(player_name)
            )

            single_muted_player_form.add_button(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, 'button.back_to_previous')}",
                icon="textures/ui/refresh_light",
                on_click=self.muted_player
            )

            player.send_form(single_muted_player_form)

        return on_click

    def unmute_player(self, player_name: str):
        def on_click(player: Player):
            self.mute_data.remove(player_name)

            self.save_mute_data()

            player.send_message(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, 'unmute.message.success').format(player_name)}"
            )

        return on_click

    def reload_configuration(self, player: Player):
        reload_configuration_form = ActionForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'reload_configuration_form.title')}",
            content=f"{ColorFormat.GREEN}"
                    f"{self.get_text(player, 'reload_configuration_form.content')}",
            on_close=self.back_to_main_form
        )

        reload_configuration_form.add_button(
            f"{ColorFormat.YELLOW}"
            f"{self.get_text(player, 'reload_configuration_form.button.variable_setting')}",
            icon="textures/ui/icon_setting",
            on_click=self.variable_setting
        )

        reload_configuration_form.add_button(
            f"{ColorFormat.YELLOW}"
            f"{self.get_text(player, 'reload_configuration_form.button.reload_global_configuration')}",
            icon="textures/ui/icon_setting",
            on_click=self.reload_global_configuration
        )

        reload_configuration_form.add_button(
            f"{ColorFormat.YELLOW}"
            f"{self.get_text(player, 'button.back_to_previous')}",
            icon="textures/ui/refresh_light",
            on_click=self.back_to_main_form
        )

        player.send_form(reload_configuration_form)

    def variable_setting(self, player: Player):
        variables_all = [
            "Health",
            "Device",
            "Money",
            "Mode",
            "Dimension",
            "Ping",
            "Level",
            "Online-time",
            "Break",
            "Place",
            "Death",
            "PVP",
            "PVE",
            "KD",
            "Pick-up",
            "Drop",
            "Move-distance"
        ]

        variables_order = self.config_data["variables_order"]

        if len(variables_order) == 0:
            variables_order = []
        else:
            variables_order = variables_order.split("++")

        variables_hide = []
        for v in variables_all:
            if v not in variables_order:
                variables_hide.append(v)

        variable_setting_form = ActionForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'variable_setting_form.title')}",
            content=f"{ColorFormat.GREEN}"
                    f"{self.get_text(player, 'variable_order')}",
            on_close=self.reload_configuration
        )

        variable_setting_form.add_button(
            f"{ColorFormat.YELLOW}"
            f"{self.get_text(player, 'button.back_to_previous')}",
            icon="textures/ui/refresh_light",
            on_click=self.reload_configuration
        )

        for variable in variables_order:
            num = variables_order.index(variable) + 1

            variable_setting_form.add_button(
                f"{ColorFormat.YELLOW}"
                f"[{num}] {self.get_text(player, variable)}",
                icon="textures/ui/icon_unlocked",
                on_click=self.edit_single_variable(variable)
            )

        for variable_hide in variables_hide:
            variable_setting_form.add_button(
                f"{ColorFormat.GRAY}"
                f"[{self.get_text(player, 'hidden')}] "
                f"{self.get_text(player, variable_hide)}",
                icon="textures/ui/icon_lock",
                on_click=self.edit_single_variable(variable_hide)
            )

        player.send_form(variable_setting_form)

    def edit_single_variable(self, variable: str):
        def on_click(player: Player):
            edit_single_variable_form = ActionForm(
                title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                      f"{variable}",
                on_close=self.variable_setting
            )

            variables_order = self.config_data["variables_order"]

            if len(variables_order) == 0:
                variables_order = []
            else:
                variables_order = variables_order.split("++")

            if variable in variables_order:
                if variables_order.index(variable) != 0:
                    edit_single_variable_form.add_button(
                        f"{ColorFormat.YELLOW}"
                        f"{self.get_text(player, 'edit_single_variable_form.button.up')}",
                        icon="textures/ui/dropdown_chevron_up",
                        on_click=self.edit_single_variable_up_or_down(variable, "up")
                    )

                if variables_order.index(variable) != -1:
                    edit_single_variable_form.add_button(
                        f"{ColorFormat.YELLOW}"
                        f"{self.get_text(player, 'edit_single_variable_form.button.down')}",
                        icon="textures/ui/dropdown_chevron",
                        on_click=self.edit_single_variable_up_or_down(variable, "down")
                    )

                edit_single_variable_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(player, 'edit_single_variable_form.button.hide')}",
                    icon="textures/ui/icon_unlocked",
                    on_click=self.edit_single_variable_hide_or_show(variable, "hide")
                )
            else:
                edit_single_variable_form.add_button(
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(player, 'edit_single_variable_form.button.show')}",
                    icon="textures/ui/icon_lock",
                    on_click=self.edit_single_variable_hide_or_show(variable, "show")
                )

            edit_single_variable_form.add_button(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, 'button.back_to_previous')}",
                icon="textures/ui/refresh_light",
                on_click=self.variable_setting
            )

            player.send_form(edit_single_variable_form)

        return on_click

    def edit_single_variable_up_or_down(self, variable: str, target: str):
        def on_click(player: Player):
            variables_order = self.config_data["variables_order"].split("++")

            original_index = variables_order.index(variable)

            if target == "up":
                new_index = original_index - 1
            else:
                new_index = original_index + 1

            variables_order.remove(variable)

            variables_order.insert(new_index, variable)

            variables_order = "++".join(variables_order)

            self.config_data["variables_order"] = variables_order

            self.save_config_data()

            self.variable_setting(player)

        return on_click

    def edit_single_variable_hide_or_show(self, variable: str, target: str):
        def on_click(player: Player):
            variables_order = self.config_data["variables_order"]

            if len(variables_order) == 0:
                variables_order = []
            else:
                variables_order = variables_order.split("++")

            if target == "hide":
                variables_order.remove(variable)
            else:
                variables_order.append(variable)

            variables_order = "++".join(variables_order)

            self.config_data["variables_order"] = variables_order

            self.save_config_data()

            self.variable_setting(player)

        return on_click

    def reload_global_configuration(self, player: Player):
        toggle1 = Toggle(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'reload_global_configuration_form.toggle1.label')}"
        )

        if self.config_data["is_set_or_update_nickname_enabled"]:
            toggle1.default_value = True
        else:
            toggle1.default_value = False

        textinput1 = TextInput(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'reload_global_configuration_form.textinput1.label')}: "
                  f"{ColorFormat.WHITE}"
                  f"{self.config_data['max_nickname_len']}",
            placeholder=self.get_text(player, 'reload_global_configuration_form.textinput1.placeholder'),
            default_value=f"{self.config_data['max_nickname_len']}"
        )

        textinput2 = TextInput(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'reload_global_configuration_form.textinput2.label')}: "
                  f"{ColorFormat.WHITE}"
                  f"{self.config_data['set_or_update_nickname_cost']}",
            placeholder=self.get_text(player, 'reload_global_configuration_form.textinput2.placeholder'),
            default_value=f"{self.config_data['set_or_update_nickname_cost']}"
        )

        toggle2 = Toggle(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'reload_global_configuration_form.toggle2.label')}"
        )

        if self.config_data["is_record_history_message_enabled"]:
            toggle2.default_value = True
        else:
            toggle2.default_value = False

        textinput3 = TextInput(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'reload_global_configuration_form.textinput3.label')}: "
                  f"{ColorFormat.WHITE}"
                  f"{self.config_data['max_history_message_num_recorded']}",
            placeholder=self.get_text(player, "reload_global_configuration_form.textinput3.placeholder"),
            default_value=f"{self.config_data['max_history_message_num_recorded']}"
        )

        toggle3 = Toggle(
            label=f"{ColorFormat.GREEN}"
                  f"{self.get_text(player, 'reload_global_configuration_form.toggle3.label')}"
        )

        if self.config_data["is_simplify_join_or_left_prompt_enabled"]:
            toggle3.default_value = True
        else:
            toggle3.default_value = False

        reload_global_configuration_form = ModalForm(
            title=f"{ColorFormat.BOLD}{ColorFormat.LIGHT_PURPLE}"
                  f"{self.get_text(player, 'reload_global_configuration_form.title')}",
            controls=[
                toggle1,
                textinput1,
                textinput2,
                toggle2,
                textinput3,
                toggle3
            ],
            submit_button=f"{ColorFormat.YELLOW}"
                          f"{self.get_text(player, 'reload_global_configuration_form.submit_button')}",
            on_close=self.reload_configuration
        )

        def on_submit(p: Player, json_str: str):
            data = json.loads(json_str)

            try:
                v2 = int(data[1])
                v3 = int(data[2])
                v5 = int(data[4])
            except:
                p.send_message(
                    f"{ColorFormat.RED}"
                    f"{self.get_text(p, 'message.error')}"
                )

                return

            if v2 <= 0 or v3 < 0 or v5 <= 0:
                p.send_message(
                    f"{ColorFormat.RED}"
                    f"{self.get_text(p, 'message.error')}"
                )

                return

            v1 = data[0]
            v4 = data[3]
            v6 = data[5]

            self.config_data["is_set_or_update_nickname_enabled"] = v1
            self.config_data["max_nickname_len"] = v2
            self.config_data["set_or_update_nickname_cost"] = v3
            self.config_data["is_record_history_message_enabled"] = v4
            self.config_data["max_history_message_num_recorded"] = v5
            self.config_data["is_simplify_join_or_left_prompt_enabled"] = v6

            self.save_config_data()

            p.send_message(
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(p, 'reload_global_configuration.message.success')}"
            )

        reload_global_configuration_form.on_submit = on_submit

        player.send_form(reload_global_configuration_form)

    def save_nickname_data(self):
        with open(nickname_data_file_path, "w+", encoding="utf-8") as f:
            json_str = json.dumps(self.nickname_data, indent=4, ensure_ascii=False)
            f.write(json_str)

    def save_mute_data(self):
        with open(mute_data_file_path, "w+") as f:
            json_str = json.dumps(self.mute_data, indent=4, ensure_ascii=False)
            f.write(json_str)

    def save_config_data(self):
        with open(config_data_file_path, "w+") as f:
            json_str = json.dumps(self.config_data, indent=4, ensure_ascii=False)
            f.write(json_str)

    def variable_handler(self, player: Player, variable: str) -> any:
        if variable == "Health":
            value = player.health

            result = (
                f"{ColorFormat.RED}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Device":
            value = player.device_os

            result = (
                f"{ColorFormat.AQUA}"
                f"{self.get_text(player, 'Device')}:"
                f"{value}"
            )
        elif variable == "Money":
            value = self.server.plugin_manager.get_plugin("umoney").api_get_player_money(player.name)

            result = (
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Mode":
            value = player.game_mode.name

            if value == "ADVENTURE":
                result = (
                    f"{ColorFormat.RED}"
                    f"{self.get_text(player, value)}"
                )
            elif value == "SURVIVAL":
                result = (
                    f"{ColorFormat.GREEN}"
                    f"{self.get_text(player, value)}"
                )
            elif value == "CREATIVE":
                result = (
                    f"{ColorFormat.YELLOW}"
                    f"{self.get_text(player, value)}"
                )
            else:
                result = (
                    f"{ColorFormat.GRAY}"
                    f"{self.get_text(player, value)}"
                )
        elif variable == "Dimension":
            value = player.location.dimension.name

            if value == "Overworld":
                result = (
                    f"{ColorFormat.GREEN}"
                    f"{self.get_text(player, value)}"
                )
            elif value == "Nether":
                result = (
                    f"{ColorFormat.RED}"
                    f"{self.get_text(player, value)}"
                )
            else:
                result = (
                    f"{ColorFormat.LIGHT_PURPLE}"
                    f"{self.get_text(player, value)}"
                )
        elif variable == "Ping":
            value = round(player.ping)

            result = (
                f"{ColorFormat.GREEN}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Level":
            value = player.exp_level

            result = (
                f"{ColorFormat.GREEN}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Online-time":
            raw_value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("online_time", player.name)

            y_m = 365 * 24 * 60
            d_m = 24 * 60
            h_m = 60

            y = raw_value // y_m
            r = raw_value % y_m

            d = r // d_m
            r %= d_m

            h = r // h_m
            m = r % h_m

            value = f"{y}Y{d}D{h}H{m}M"

            result = (
                f"{ColorFormat.AQUA}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Break":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("break_count", player.name)

            result = (
                f"{ColorFormat.LIGHT_PURPLE}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Place":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("place_count", player.name)

            result = (
                f"{ColorFormat.LIGHT_PURPLE}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Death":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("death_count", player.name)

            result = (
                f"{ColorFormat.RED}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "PVP":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("kill_player_count", player.name)

            result = (
                f"{ColorFormat.RED}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "PVE":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("kill_mob_count", player.name)

            result = (
                f"{ColorFormat.RED}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "KD":
            value1: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("kill_player_count", player.name)

            value2: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("death_count", player.name)

            if value1 == 0 or value2 == 0:
                value = 0.0
            else:
                value = round(value1 / value2, 1)

            result = (
                f"{ColorFormat.RED}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Pick-up":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("pick_up_item_count", player.name)

            result = (
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Drop":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("drop_item_count", player.name)

            result = (
                f"{ColorFormat.YELLOW}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        elif variable == "Move-distance":
            value: int = self.server.plugin_manager.get_plugin("ustatistic").api_get_player_statistical_data("move_distance_data", player.name)

            result = (
                f"{ColorFormat.LIGHT_PURPLE}"
                f"{self.get_text(player, variable)}:"
                f"{value}"
            )
        else:
            result = ""

        return result

    @event_handler
    def on_player_chat(self, e: PlayerChatEvent):
        if e.player.name in self.mute_data:
            e.cancel()

            e.player.send_message(
                f"{ColorFormat.RED}"
                f"{self.get_text(e.player, 'message.muted')}"
            )

            return

        variables_order = self.config_data["variables_order"]

        if len(variables_order) == 0:
            variables_order = []
        else:
            variables_order = variables_order.split("++")

        if len(variables_order) != 0:
            pre = (
                f"{ColorFormat.WHITE}"
                f"["
            )

            for variable in variables_order:
                result = self.variable_handler(e.player, variable)

                if result:
                    pre += result

                    if variables_order.index(variable) == len(variables_order) - 1:
                        pre += (
                            f"{ColorFormat.WHITE}"
                            f"]"
                        )
                    else:
                        pre += (
                            f"{ColorFormat.WHITE}"
                            f" | "
                        )
        else:
            pre = ""

        unique_nickname = self.nickname_data[e.player.name]["unique_nickname"]

        if unique_nickname:
            pre += f' {ColorFormat.WHITE}@{unique_nickname}{ColorFormat.RESET}'

        nickname = self.nickname_data[e.player.name]["nickname"]

        if nickname:
            pre += f' {ColorFormat.WHITE}[{nickname}]{ColorFormat.RESET}'

        e.format = f"{pre} {e.player.name} >> {e.message}"

        if self.config_data["is_record_history_message_enabled"]:
            message_datetime = str(datetime.datetime.now()).split(".")[0]

            message_to_record = f"[{message_datetime}] {e.player.name} >> {e.message}"

            if len(self.message_recorder) == self.config_data["max_history_message_num_recorded"]:
                self.message_recorder.pop(0)

            self.message_recorder.append(message_to_record)

    @event_handler
    def on_player_join(self, e: PlayerJoinEvent):
        if self.nickname_data.get(e.player.name) is None:
            self.nickname_data[e.player.name] = {
                "nickname": "",
                "unique_nickname": ""
            }

            self.save_nickname_data()

        join_message = e.join_message

        e.join_message = None

        if self.config_data["is_simplify_join_or_left_prompt_enabled"]:
            self.server.broadcast_message(
                f"{ColorFormat.GREEN}[+] {ColorFormat.WHITE}{e.player.name}"
            )

            self.server.dispatch_command(
                self.command_sender_wrapper,
                "playsound note.bell @a"
            )
        else:
            self.server.broadcast_message(join_message)

        if len(self.message_recorder) != 0:
            for m in self.message_recorder:
                e.player.send_message(m)

    @event_handler
    def on_player_left(self, e: PlayerQuitEvent):
        if self.config_data["is_simplify_join_or_left_prompt_enabled"]:
            e.quit_message = (
                f"{ColorFormat.RED}[-] {ColorFormat.WHITE}{e.player.name}"
            )

            self.server.dispatch_command(
                self.command_sender_wrapper,
                "playsound note.guitar @a"
            )

    def get_text(self, player: Player, text_key: str) -> str:
        player_lang = player.locale

        try:
            if self.lang_data.get(player_lang) is None:
                text_value = self.lang_data["en_US"][text_key]
            else:
                if self.lang_data[player_lang].get(text_key) is None:
                    text_value = self.lang_data["en_US"][text_key]
                else:
                    text_value = self.lang_data[player_lang][text_key]

            return text_value
        except Exception as e:
            self.logger.error(
                f"{ColorFormat.RED}"
                f"{e}"
            )

            return text_key

    def back_to_main_form(self, player: Player):
        player.perform_command("ubc")

    def back_to_zx_ui(self, player: Player):
        player.perform_command("cd")

    # API
    def api_get_player_nickname(self, player_name: str) -> str:
        nickname: str = self.nickname_data[player_name]["nickname"]

        return nickname

    def api_get_player_unique_nickname(self, player_name: str) -> str:
        unique_nickname: str = self.nickname_data[player_name]["unique_nickname"]

        return unique_nickname



