import os
import json


def load_lang_data(lang_dir: str) -> dict:
    zh_CN_file_path = os.path.join(lang_dir, "zh_CN.json")
    en_US_file_path = os.path.join(lang_dir, "en_US.json")

    if not os.path.exists(zh_CN_file_path):
        with open(zh_CN_file_path, "w", encoding="utf-8") as f:
            zh_CN ={
                "message.error": "表单解析错误, 请按提示正确填写...",
                "message.muted": "你已被本服务器禁言...",

                "money": "余额",
                "nickname": "昵称",
                "unique_nickname": "特殊昵称",
                "set_or_update_nickname_cost": "耗费 (设置|更新)",

                "button.back_to_zx_ui": "返回",
                "button.close": "关闭",
                "button.back_to_previous": "返回",

                "main_form.title": "U-Beautiful-Chat - 主表单",
                "main_form.content": "请选择操作...",
                "main_form.button.set_nickname": "设置昵称",
                "main_form.button.set_unique_nickname": "设置特殊昵称",
                "main_form.button.muted_player": "被禁言的玩家",
                "main_form.button.reload_config": "重载配置文件",

                "set_nickname_form.textinput.label": "输入昵称...",
                "set_nickname_form.textinput.placeholder": "输入任意不超过 {0} 个字符的字符串或留空...",
                "set_nickname_form.title": "设置昵称",
                "set_nickname_form.submit_button": "设置",
                "set_nickname.message.success": "设置昵称成功...",

                "set_unique_nickname_form.dropdown": "选择玩家...",
                "set_unique_nickname_form.title": "设置特殊昵称",
                "set_unique_nickname_form.submit_button": "选择",
                "set_unique_nickname_form1.textinput.label1": "你正在为玩家: {0} 设置特殊昵称...",
                "set_unique_nickname_form1.textinput.label2": "输入特殊昵称...",
                "set_unique_nickname_form1.textinput.placeholder": "输入任意字符串或留空....",
                "set_unique_nickname_form1.title": "设置特殊昵称",
                "set_unique_nickname_form1.submit_button": "设置",
                "set_unique_nickname.message.success": "为玩家: {0} 设置特殊昵称成功...",

                "muted_player_form.title": "被禁言的玩家",
                "muted_player_form.content": "请选择操作...",
                "muted_player_form.button.mute_player": "禁言玩家",

                "mute_player_form.dropdown.label": "选择玩家...",
                "mute_player_form.title": "禁言玩家",
                "mute_player_form.submit_button": "禁言",
                "mute_player.message.success": "禁言玩家: {0} 成功...",
                "mute_player.message.fail": "没有可用于禁言的玩家...",

                "single_muted_player_form.content": "请选择操作...",
                "single_muted_player_form.button.unmute": "解除禁言",

                "unmute.message.success": "为玩家: {0} 解除禁言成功...",

                "reload_configuration_form.title": "重载配置文件",
                "reload_configuration_form.content": "请选择操作...",
                "reload_configuration_form.button.variable_setting": "变量设置",
                "reload_configuration_form.button.reload_global_configuration": "重载全局配置文件",

                "variable_setting_form.title": "变量设置",
                "variable_order": "变量顺序",

                "edit_single_variable_form.button.up": "向上",
                "edit_single_variable_form.button.down": "向下",
                "edit_single_variable_form.button.hide": "隐藏",
                "edit_single_variable_form.button.show": "显示",

                "reload_global_configuration_form.toggle1.label": "是否启用 设置|更新 昵称?",
                "reload_global_configuration_form.textinput1.label": "当前单个昵称的最大长度",
                "reload_global_configuration_form.textinput1.placeholder": "输入一个正整数...",
                "reload_global_configuration_form.textinput2.label": "当前 设置|更新 一个昵称的耗费",
                "reload_global_configuration_form.textinput2.placeholder": "输入一个正整数或0...",
                "reload_global_configuration_form.toggle2.label": "是否启用记录历史消息?",
                "reload_global_configuration_form.textinput3.label": "当前将被记录的历史消息的最大数量",
                "reload_global_configuration_form.textinput3.placeholder": "输入一个正整数...",
                "reload_global_configuration_form.toggle3.label": "是否启用 加入|退出 简化提示词?",
                "reload_global_configuration_form.title": "重载全局配置文件",
                "reload_global_configuration_form.submit_button": "重载",
                "reload_global_configuration.message.success": "重载全局配置文件成功...",

                "Health": "生命",
                "Device": "设备",
                "Money": "金币",
                "Mode": "模式",
                "ADVENTURE": "冒险",
                "SURVIVAL": "生存",
                "CREATIVE": "创造",
                "SPECTATOR": "旁观",
                "Dimension": "维度",
                "Overworld": "主世界",
                "Nether": "地狱",
                "Theend": "末地",
                "Ping": "延迟",
                "Level": "等级",
                "Online-time": "在线时长",
                "Break": "破坏",
                "Place": "放置",
                "Death": "死亡",
                "PVP": "PVP",
                "PVE": "PVE",
                "KD": "KD",
                "Pick-up": "拾取",
                "Drop": "丢弃",
                "Move-distance": "移动距离",

                "hidden": "隐藏"
            }
            json_str = json.dumps(zh_CN, indent=4, ensure_ascii=False)
            f.write(json_str)

    if not os.path.exists(en_US_file_path):
        with open(en_US_file_path, "w", encoding="utf-8") as f:
            en_US = {
                "message.error": "The form is parsed incorrectly, please follow the prompts to fill in correctly...",
                "message.muted": "You have been muted by this server...",

                "money": "your money",
                "nickname": "Nickname",
                "unique_nickname": "Unique nickname",
                "set_or_update_nickname_cost": "Cost (set|update)",

                "button.back_to_zx_ui": "Back",
                "button.close": "Close",
                "button.back_to_previous": "Back to previous",

                "main_form.title": "U-Beautiful-Chat - main form",
                "main_form.content": "Please select a function...",
                "main_form.button.set_nickname": "Set nickname",
                "main_form.button.set_unique_nickname": "Set unique nickname",
                "main_form.button.muted_player": "Muted player(s)",
                "main_form.button.reload_config": "Reload configurations",

                "set_nickname_form.textinput.label": "Input nickname...",
                "set_nickname_form.textinput.placeholder": "Input any string not more than {0} chars or left blank...",
                "set_nickname_form.title": "Set nickname",
                "set_nickname_form.submit_button": "Set",
                "set_nickname.message.success": "Successfully set nickname...",

                "set_unique_nickname_form.dropdown": "Select a player...",
                "set_unique_nickname_form.title": "Set unique nickname",
                "set_unique_nickname_form.submit_button": "Select",
                "set_unique_nickname_form1.textinput.label1": "You are setting unique nickname for player: {0}...",
                "set_unique_nickname_form1.textinput.label2": "Input unique nickname...",
                "set_unique_nickname_form1.textinput.placeholder": "Input any string or left blank....",
                "set_unique_nickname_form1.title": "Set unique nickname",
                "set_unique_nickname_form1.submit_button": "Set",
                "set_unique_nickname.message.success": "Successfully set unique nickname for player: {0}...",

                "muted_player_form.title": "Muted player(s)",
                "muted_player_form.content": "Please select a function...",
                "muted_player_form.button.mute_player": "Mute a player",

                "mute_player_form.dropdown.label": "Please select a player...",
                "mute_player_form.title": "Mute a player",
                "mute_player_form.submit_button": "Mute",
                "mute_player.message.success": "Successfully muted player: {0}...",
                "mute_player.message.fail": "There are no players available to mute...",

                "single_muted_player_form.content": "Please select a function...",
                "single_muted_player_form.button.unmute": "Unmute",

                "unmute.message.success": "Successfully unmuted player: {0}...",

                "reload_configuration_form.title": "Reload configurations",
                "reload_configuration_form.content": "Please select a function...",
                "reload_configuration_form.button.variable_setting": "Variables settings",
                "reload_configuration_form.button.reload_global_configuration": "Reload global configurations",

                "variable_setting_form.title": "Variables settings",
                "variable_order": "variables order",

                "edit_single_variable_form.button.up": "Up",
                "edit_single_variable_form.button.down": "Down",
                "edit_single_variable_form.button.hide": "Hide",
                "edit_single_variable_form.button.show": "Show",

                "reload_global_configuration_form.toggle1.label": "is set|update nickname enabled?",
                "reload_global_configuration_form.textinput1.label": "The current max length for a nickname",
                "reload_global_configuration_form.textinput1.placeholder": "Input a positive integer...",
                "reload_global_configuration_form.textinput2.label": "The current cost to set|update a nickname",
                "reload_global_configuration_form.textinput2.placeholder": "Input a positive integer or zero...",
                "reload_global_configuration_form.toggle2.label": "is record history message enabled?",
                "reload_global_configuration_form.textinput3.label": "The current max number of history messages to be recorded",
                "reload_global_configuration_form.textinput3.placeholder": "Input a positive integer...",
                "reload_global_configuration_form.toggle3.label": "is simplify join|left prompt enabled?",
                "reload_global_configuration_form.title": "Reload global configurations",
                "reload_global_configuration_form.submit_button": "Reload",
                "reload_global_configuration.message.success": "Successfully reloaded global configurations...",

                "Health": "Health",
                "Device": "Device",
                "Money": "Money",
                "Mode": "Mode",
                "ADVENTURE": "Adventure",
                "SURVIVAL": "Survival",
                "CREATIVE": "Creative",
                "SPECTATOR": "Spectator",
                "Dimension": "Dimension",
                "Overworld": "Overworld",
                "Nether": "Nether",
                "Theend": "The end",
                "Ping": "Ping",
                "Level": "Level",
                "Online-time": "Online-time",
                "Break": "Break",
                "Place": "Place",
                "Death": "Death",
                "PVP": "PVP",
                "PVE": "PVE",
                "KD": "KD",
                "Pick-up": "Pick-up",
                "Drop": "Drop",
                "Move-distance": "Move-distance",

                "hidden": "Hidden"
            }
            json_str = json.dumps(en_US, indent=4, ensure_ascii=False)
            f.write(json_str)

    lang_data = {}

    for lang in os.listdir(lang_dir):
        lang_name = lang.strip(".json")

        lang_file_path = os.path.join(lang_dir, lang)

        with open(lang_file_path, "r", encoding="utf-8") as f:
            lang_data[lang_name] = json.loads(f.read())

    return lang_data
