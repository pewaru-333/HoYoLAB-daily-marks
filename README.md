<div align="center">
    <img width="128" height="128" src="assets/icon.svg" alt="icon">
</div>


<div align="center">

# HoYoLAB daily rewards

</div>

This is a rewritten version of the [hoyolab-auto-sign](https://github.com/canaria3406/hoyolab-auto-sign) script in Python, which supports only making daily check-in marks without any external notifications.

## Configuration

```Python
profile = {
    "ltoken_v2": "Obtained ltoken_v2",
    "ltuid_v2": "Obtained ltuid_v2",
    "genshin": True,
    "honkai_star_rail": False,
    "honkai_3": False,
    "tears_of_themis": False,
    "zenless_zone_zero": False,
    "account_name": "Your account name (can be anything at all)",
    "locale": "Prefer to use two lowercase letters locale (for example: ru)"
}
```

Locale parameter affects the language of receiving notifications about the check-in in the game. See [this screenshot](assets/locale_screenshot.png).

To get the necessary `ltoken_v2` and `ltuid_v2`, please, follow the instructions provided here: https://github.com/Joshua-Noakes1/mei-cards#2-getting-your-hoyolab-cookies.


## Usage example

If you have a router with Entware installed, you can set up a daily task to automatically check-in.

1. Connect to Entware with SSH or Telnet.

```bash
ssh [router address] -p [port] -l [username]
```

2. Install necessary packages.

```bash
opkg install python3
opkg install python3-pip
opkg install cron
pip install requests
```

3. Create a folder somewhere in your Entware and put a [script.py](script.py) there. You can use the SMB explorer to do this more easily. The approximate path is shown below.

```
/opt/etc/hoyolab/script.py
```

4. Open script.py as text and replace fields in profile dict. Test script.

```bash
/opt/bin/python3 /opt/etc/hoyolab/script.py
```

5. If you get message in terminal (not Python exceptions), then setup cron. Open this file

```
/opt/etc/crontab
```

and put this line at the end

```
05 19 * * * root /opt/bin/python3 /opt/etc/hoyolab/script.py > /opt/etc/hoyolab/log.txt 2>&1
```

where first two digits are minutes, second pair is hours. This code `/opt/etc/hoyolab/log.txt 2>&1` creates a file with log.

6. Start cron service

```bash
/opt/etc/init.d/S10cron start
```

7. As the result, you can see this text in `log.txt`.

```
======= Check-in for Player =======
Check-in for Genshin Impact is successful!
```
