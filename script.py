from time import sleep

import requests

profile = {
    "ltoken_v2": "Obtained ltoken_v2",
    "ltuid_v2": "Obtained ltuid_v2",
    "genshin": True,
    "honkai_star_rail": False,
    "honkai_3": False,
    "tears_of_themis": False,
    "zenless_zone_zero": False,
    "account_name": "Your account name (can be anything at all)"
}

url_dict = {
    "Genshin": 'https://sg-hk4e-api.hoyolab.com/event/sol/sign?lang=en-us&act_id=e202102251931481',
    "Star_Rail": 'https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=en-us&act_id=e202303301540311',
    "Honkai_3": 'https://sg-public-api.hoyolab.com/event/mani/sign?lang=en-us&act_id=e202110291205111',
    "Tears_of_Themis": 'https://sg-public-api.hoyolab.com/event/luna/os/sign?lang=en-us&act_id=e202308141137581',
    "Zenless_Zone_Zero": 'https://sg-public-api.hoyolab.com/event/luna/zzz/os/sign?lang=en-us&act_id=e202406031448091'
}

header_dict = {
    "default": {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'x-rpc-app_version': '2.34.1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-rpc-client_type': '4',
        'Referer': 'https://act.hoyolab.com/',
        'Origin': 'https://act.hoyolab.com',
    },
    "Genshin": {

    },
    "Star_Rail": {

    },
    "Honkai_3": {

    },
    "Tears_of_Themis": {

    },
    "Zenless_Zone_Zero": {
        'x-rpc-signgame': 'zzz',
    }
}


def auto_sign_in():
    urls_with_headers = []

    if profile.get("genshin"):
        urls_with_headers.append(
            dict(
                url=url_dict["Genshin"],
                headers={
                    **header_dict["default"], **header_dict["Genshin"]
                }
            )
        )

    if profile.get("honkai_star_rail"):
        urls_with_headers.append(
            dict(
                url=url_dict["Star_Rail"],
                headers={
                    **header_dict["default"], **header_dict["Star_Rail"]
                }
            )
        )

    if profile.get("honkai_3"):
        urls_with_headers.append(
            dict(
                url=url_dict["Honkai_3"],
                headers={
                    **header_dict["default"], **header_dict["Honkai_3"]
                }
            )
        )

    if profile.get("tears_of_themis"):
        urls_with_headers.append(
            dict(
                url=url_dict["Tears_of_Themis"],
                headers={
                    **header_dict["default"], **header_dict["Tears_of_Themis"]
                }
            )
        )

    if profile.get("zenless_zone_zero"):
        urls_with_headers.append(
            dict(
                url=url_dict["Zenless_Zone_Zero"],
                headers={
                    **header_dict["default"], **header_dict["Zenless_Zone_Zero"]
                }
            )
        )

    response_message = f"Check-in completed for {profile['account_name']}"

    sleep_time = 5
    sign_in_requests = []

    for item in urls_with_headers:
        sleep(sleep_time)

        request = requests.post(
            url=item["url"],
            headers=item["headers"],
            cookies={
                "ltoken_v2": profile["ltoken_v2"],
                "ltuid_v2": profile["ltuid_v2"]
            },
            allow_redirects=False
        )

        sign_in_requests.append(request)

    for index, response in enumerate(sign_in_requests):

        game_name = next((key for key, value in url_dict.items() if value == urls_with_headers[index]["url"]), None)
        game_name = game_name.replace("_", " ") if game_name else ""

        try:
            response_json = response.json()
            check_in_result = response_json.get("message")
            is_error = check_in_result != "OK"

            if is_error:
                try:
                    captcha_blocked = (
                        response_json
                        .get("data")
                        .get("gt_result")
                        .get("is_risk")
                    )

                    if captcha_blocked:
                        response_message += f"\n{game_name}: Auto check-in failed due to CAPTCHA blocking."

                except Exception:
                    response_message += f"\n{game_name}: {'' if not is_error else '@everyone'} {check_in_result}"


        except Exception as e:
            response_message += f"\nError processing {game_name}: {str(e)}"

    print(response_message)


if __name__ == "__main__":
    auto_sign_in()
