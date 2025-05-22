from time import sleep

import requests
from requests import Response

profile = {
    "ltoken_v2": "Obtained ltoken_v2",
    "ltuid_v2": "Obtained ltuid_v2",
    "genshin": True,
    "honkai_star_rail": False,
    "honkai_3": False,
    "tears_of_themis": False,
    "zenless_zone_zero": False,
    "account_name": "Your account name (can be anything at all)",
    "locale": "ru"  # [en-us, de, es, fr, it, pt, ru, tr, zh-cn, zh-tw, ja, ko, id, th, vi]
}

games = {
    "Genshin Impact": {
        "is_picked": profile["genshin"],
        "link": {
            "url": "https://sg-hk4e-api.hoyolab.com/event/sol/sign",
            "params": {
                "lang": profile["locale"],
                "act_id": "e202102251931481"
            },
            "headers": {}
        }
    },
    "Honkai Star Rail": {
        "is_picked": profile["honkai_star_rail"],
        "link": {
            "url": "https://sg-public-api.hoyolab.com/event/luna/os/sign",
            "params": {
                "lang": profile["locale"],
                "act_id": "e202303301540311"
            },
            "headers": {}
        }
    },
    "Honkai Impact 3rd": {
        "is_picked": profile["honkai_3"],
        "link": {
            "url": "https://sg-public-api.hoyolab.com/event/mani/sign",
            "params": {
                "lang": profile["locale"],
                "act_id": "e202110291205111"
            },
            "headers": {}
        }
    },
    "Tears of Themis": {
        "is_picked": profile["tears_of_themis"],
        "link": {
            "url": "https://sg-public-api.hoyolab.com/event/luna/os/sign",
            "params": {
                "lang": profile["locale"],
                "act_id": "e202308141137581"
            },
            "headers": {}
        }
    },
    "Zenless Zone Zero": {
        "is_picked": profile["zenless_zone_zero"],
        "link": {
            "url": "https://sg-public-api.hoyolab.com/event/luna/zzz/os/sign",
            "params": {
                "lang": profile["locale"],
                "act_id": "e202406031448091"
            },
            "headers": {
                "x-rpc-signgame": "zzz"
            }
        }
    }
}

common_header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Origin": "https://act.hoyolab.com",
    "Referer": "https://act.hoyolab.com/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3",
    "x-rpc-app_version": "2.34.1",
    "x-rpc-client_type": "4"
}


def auto_sign_in():
    print(f"======= Check-in for {profile['account_name']} =======")

    picked_games = {key: value for key, value in games.items() if value["is_picked"]}
    responses: dict[str, Response] = {}

    for key, value in picked_games.items():
        sleep(5)

        request = requests.post(
            url=value["link"]["url"],
            params=value["link"]["params"],
            headers={
                **value["link"]["headers"],
                **common_header
            },
            cookies={
                "ltoken_v2": profile["ltoken_v2"],
                "ltuid_v2": profile["ltuid_v2"]
            },
            allow_redirects=False
        )

        responses[key] = request

    response_message = ""

    for game, response in responses.items():
        try:
            response_json = response.json()
            check_in_result: str = response_json.get("message")
            is_error = check_in_result != "OK"

            if not is_error:
                response_message += f"Check-in for {game} is successful!\n"
            else:
                if response_json.get("data") is None:
                    response_message += f"{game}: {check_in_result}\n"
                else:
                    try:
                        captcha_blocked = response_json["data"]["gt_result"]["is_risk"]

                        if captcha_blocked:
                            response_message += f"{game}: Auto check-in failed due to CAPTCHA blocking!\n"

                    except Exception:
                        response_message += f"{game}: Unexpected error!\n"

        except Exception as e:
            response_message += f"Error processing {game}: {str(e)}\n"

    print(response_message)


if __name__ == "__main__":
    auto_sign_in()
