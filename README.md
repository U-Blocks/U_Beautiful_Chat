<code><a href="https://github.com/umarurize/U_Beautiful_Chat"><img height="25" src="./logo/ubc.png" alt="U-Beautiful-Chat" /></a>&nbsp;U-Beautiful-Chat</code>

![Total Git clones](https://img.shields.io/badge/dynamic/json?label=Total%20Git%20clones&query=$&url=https://cdn.jsdelivr.net/gh/umarurize/U_Beautiful_Chat@master/clone_count.txt&color=brightgreen)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/umarurize/U_Beautiful_Chat/total)
![](https://img.shields.io/badge/language-python-blue.svg) 
[![GitHub License](https://img.shields.io/github/license/umarurize/UTP)](LICENSE)

### ✨Introductions
<details>
<summary>17 types of variables</summary>

- [x] Health
- [x] Device
- [x] Money
- [x] Mode
- [x] Dimension
- [x] Ping
- [x] Level
- [x] Online-time
- [x] Break
- [x] Place
- [x] Death
- [x] PVP
- [x] PVE
- [x] KD
- [x] Pick-up
- [x] Drop
- [x] Move-distance

</details>

* **2 types of nicknames**
  * Nickname
  * Unique nickname (operators)
* **History messages recorder**
* **Simplify join/left prompts**
* **Free of tedious file editing**
* **Support with full GUI forms**
* **Support with hot reloading**
* **Support with localized multi-language**

<div style="width: 100%; text-align: left;">
  <img src="./logo/ubc1.jpg" style="max-width: 100%;;">
</div>

### 📦Installation
<details>
<summary>Check your Endstone's version</summary>

* **Endstone 0.10.5+**
  * 251220

</details>

<details>
<summary>Check your pre-plugins</summary>

* **Optional pre-plugins**
  * [ZX_UI](https://www.minebbs.com/resources/zx-ui.9830/)
* **Required pre-plugins**
  * [UMoney](https://github.com/U-Blocks/UMoney)
  * [UStatistic](https://github.com/U-Blocks/UStatistic)

</details>

1. Ensure you have downloaded the correct version and installed all required pre-plugins
2. Place the `.whl` file into your server's `plugins` folder
3. Restart your server
4. Enter the command `/ubc` to call out the main form of U-Beautiful-Chat

### 📄File structure
```
plugins/
├─ u-beautiful-chat/
│  ├─ config.json
│  ├─ nickname.json
│  ├─ lang/
│  │  ├─ zh_CN.json
│  │  ├─ en_US.json
```

### ⚙️Configuration
`config.json`
```json5
{
    "variables_order": "",
    "is_set_or_update_nickname_enabled": true, // If set to true, all players can set/update their nickname
    "set_or_update_nickname_cost": 10,
    "max_nickname_len": 10, // The max num of chars a nickname can achieve
    "is_record_history_message_enabled": true,
    /**
    If set to true,
    players' messages will be recorded by the server,
    and the server will send all recorded history messages to a newly joined player
    **/
    "max_history_message_num_recorded": 15, // The max num of players' messages will be stored by the server
    "is_simplify_join_or_left_prompt_enabled": true,
    /**
    If set to true,
    player join prompts will be displayed as "[+] {player_name}",
    and player left prompts will be displayed as "[-] {player_name}".
    
    In addition, the server will play sound to all players,
    note.bell for join event, and note.guitar for left event
    **/
}
```

`nickname.json`
```json5
{
    "umaru rize": {
        "nickname": "doge_cmd",
        "unique_nickname": "Server owner"
    }
}
```

### 🌎Localized multi-language
* Currently supported localized languages for U-Beautiful-Chat:
- [x] `zh_CN`
- [x] `en_US`
* How to add more languages to U-Beautiful-Chat? Here we use Japanese for an example.
  * Create a file named `ja_JP.json` and place it into `lang` folder
  * Copy all key-value pairs from `en_US.json` and paste them into `ja_JP.json`
  * Refer to the English values and translate them all into Japanese, then save the file.
  * Restart your server, and you're all done!
* If you'd like your translated language to be included as one of the official languages of this plugin, feel free to shoot over a PR.

### 💪API
```python
# Read only
# Get the specified players' nickname
self.server.plugin_manager.get_plugin("u_beautiful_chat").api_get_player_nickname(player_name: str) -> str

# Get the specified players' unique nickname
self.server.plugin_manager.get_plugin("u_beautiful_chat").api_get_player_unique_nickname(player_name: str) -> str
```

### 🎨Screenshots
You can view related screenshots of U-Beautiful-Chat from images folder of this repo.