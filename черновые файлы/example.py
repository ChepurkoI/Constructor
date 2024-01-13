import requests
import pprint
import json


cookies = {
    'current_path': '770591a82eac573c81299ae0ad0376cc39f806c898c91408f3aacacdbf723d85a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A130%3A%22%7B%22city%22%3A%22884019c7-cf52-11de-b72b-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041a%5Cu0440%5Cu0430%5Cu0441%5Cu043d%5Cu043e%5Cu0434%5Cu0430%5Cu0440%22%2C%22method%22%3A%22url%22%7D%22%3B%7D',
    'phonesIdent': '692b349e2b153bf7cd0fc78427727c2a04358dceb724753f2e7d7bc7b1f3b1c8a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%222fe8da28-814a-48f4-a2a7-2dada75df5fc%22%3B%7D',
    'ipp_uid': '1669320647926/bjW3JsE1vQtCc8ie/jQw5T9BZknoaB4/DNkOmXA==',
    'rrpvid': '815479684869625',
    'rcuid': '637fcfca322526fbf769633b',
    '_ym_uid': '1669320652745670771',
    '_ym_d': '1669320652',
    'tmr_lvid': '2397a08e40e41aee7fd441b31fdaa029',
    'tmr_lvidTS': '1669320651932',
    'cartUserCookieIdent_v3': 'f68a00b56a766cce277b4261dea0e282247ce3077fa57e887869581a9551cb6da%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22eba824c0-7202-3abc-939d-1ad36af9acd1%22%3B%7D',
    'cookieImagesUploadId': '5164e5af779192f694ce9e67e3ebd6345b63afd0491682e276a758015afc1197a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22cookieImagesUploadId%22%3Bi%3A1%3Bs%3A36%3A%2233d90823-64ff-4fe4-9b51-f50fa91bd595%22%3B%7D',
    'wishlist-login-modal-closed': 'ff901f4001cd778cc41e342bacdadbc5fc61df79b3830bb055fb2be93a44dc33a%3A2%3A%7Bi%3A0%3Bs%3A27%3A%22wishlist-login-modal-closed%22%3Bi%3A1%3Bb%3A1%3B%7D',
    'rerf': 'AAAAAGQA03htuxfEAxolAg==',
    '_gcl_au': '1.1.732804087.1677775740',
    '_ga_FLS4JETDHW': 'GS1.1.1677775740.6.0.1677775740.60.0.0',
    '_ga': 'GA1.2.1358613154.1669320650',
    'spid': '1678372287559_bcc0316a64dfa58aca1b047b3bfacf83_x4nmot90qkdxb4s2',
    'PHPSESSID': '87d3d209fe4f88dd56bbc60a6fa37cb8',
    '_gaexp': 'GAX1.2.Uo8OYhgyRvyI9jNbUapMXA.19523.1',
    '_gid': 'GA1.2.1792640292.1680175221',
    '_ym_isad': '2',
    '_ab_': '%7B%22search-design%22%3A%22new%22%2C%22search-checkbox%22%3A%22SEARCH_IN_STOCK%22%7D',
    'lang': 'ru',
    '_ym_visorc': 'b',
    '_csrf': 'af53258477e4a824d3c304f235ee67b8d9386bfeab1d68391d26facccf55d4efa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22O10mEEUL8r_TTe7ibse1DajZrsEkJUPn%22%3B%7D',
    'tmr_detect': '0%7C1680196680268',
    'ipp_key': 'v1680196973784/v33947245ba5adc7a72e273/kQorlRnSgZD6Xgeig2EbIg==',
    'rr-testCookie': 'testvalue',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Yandex";v="22"',
    'X-CSRF-Token': 'wakipbip1JPGvMS4HItPPcHgweMYQhN8u2_1Qc3RtO-OmBLI_eyB3_7Om-xI7nhUo5Ok0lwjeSbJHLAqh4TkgQ==',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.132 YaBrowser/22.3.1.899 (beta) Yowser/2.5 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'Accept': '*/*',
    'Origin': 'https://www.dns-shop.ru',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/no-referrer',
    'Accept-Language': 'ru,en;q=0.9',
    # 'Cookie': 'current_path=770591a82eac573c81299ae0ad0376cc39f806c898c91408f3aacacdbf723d85a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A130%3A%22%7B%22city%22%3A%22884019c7-cf52-11de-b72b-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu041a%5Cu0440%5Cu0430%5Cu0441%5Cu043d%5Cu043e%5Cu0434%5Cu0430%5Cu0440%22%2C%22method%22%3A%22url%22%7D%22%3B%7D; phonesIdent=692b349e2b153bf7cd0fc78427727c2a04358dceb724753f2e7d7bc7b1f3b1c8a%3A2%3A%7Bi%3A0%3Bs%3A11%3A%22phonesIdent%22%3Bi%3A1%3Bs%3A36%3A%222fe8da28-814a-48f4-a2a7-2dada75df5fc%22%3B%7D; ipp_uid=1669320647926/bjW3JsE1vQtCc8ie/jQw5T9BZknoaB4/DNkOmXA==; rrpvid=815479684869625; rcuid=637fcfca322526fbf769633b; _ym_uid=1669320652745670771; _ym_d=1669320652; tmr_lvid=2397a08e40e41aee7fd441b31fdaa029; tmr_lvidTS=1669320651932; cartUserCookieIdent_v3=f68a00b56a766cce277b4261dea0e282247ce3077fa57e887869581a9551cb6da%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22eba824c0-7202-3abc-939d-1ad36af9acd1%22%3B%7D; cookieImagesUploadId=5164e5af779192f694ce9e67e3ebd6345b63afd0491682e276a758015afc1197a%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22cookieImagesUploadId%22%3Bi%3A1%3Bs%3A36%3A%2233d90823-64ff-4fe4-9b51-f50fa91bd595%22%3B%7D; wishlist-login-modal-closed=ff901f4001cd778cc41e342bacdadbc5fc61df79b3830bb055fb2be93a44dc33a%3A2%3A%7Bi%3A0%3Bs%3A27%3A%22wishlist-login-modal-closed%22%3Bi%3A1%3Bb%3A1%3B%7D; rerf=AAAAAGQA03htuxfEAxolAg==; _gcl_au=1.1.732804087.1677775740; _ga_FLS4JETDHW=GS1.1.1677775740.6.0.1677775740.60.0.0; _ga=GA1.2.1358613154.1669320650; spid=1678372287559_bcc0316a64dfa58aca1b047b3bfacf83_x4nmot90qkdxb4s2; PHPSESSID=87d3d209fe4f88dd56bbc60a6fa37cb8; _gaexp=GAX1.2.Uo8OYhgyRvyI9jNbUapMXA.19523.1; _gid=GA1.2.1792640292.1680175221; _ym_isad=2; _ab_=%7B%22search-design%22%3A%22new%22%2C%22search-checkbox%22%3A%22SEARCH_IN_STOCK%22%7D; lang=ru; _ym_visorc=b; _csrf=af53258477e4a824d3c304f235ee67b8d9386bfeab1d68391d26facccf55d4efa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22O10mEEUL8r_TTe7ibse1DajZrsEkJUPn%22%3B%7D; tmr_detect=0%7C1680196680268; ipp_key=v1680196973784/v33947245ba5adc7a72e273/kQorlRnSgZD6Xgeig2EbIg==; rr-testCookie=testvalue',
}

data = 'data={"type":"product-buy","containers":[{"id":"as--Yko2P","data":{"id":"5066442"}},{"id":"as-mu5VE_","data":{"id":"1633582"}},{"id":"as-GHPSUM","data":{"id":"1633587"}},{"id":"as-7iL0U7","data":{"id":"5066472"}},{"id":"as-f3Bg58","data":{"id":"4793015"}},{"id":"as-oUNvPj","data":{"id":"4856291"}},{"id":"as-q725pM","data":{"id":"4726183"}},{"id":"as-eDgYQm","data":{"id":"4875266"}},{"id":"as-UNGZj7","data":{"id":"4829226"}},{"id":"as-IvURhk","data":{"id":"4829223"}},{"id":"as-BLDEs0","data":{"id":"4793040"}},{"id":"as-rYNUPQ","data":{"id":"4793041"}},{"id":"as-6f0Nbi","data":{"id":"4793043"}},{"id":"as-oy0_PG","data":{"id":"5013925"}},{"id":"as-I646S3","data":{"id":"5016001"}},{"id":"as-NE3oSB","data":{"id":"5016000"}},{"id":"as-JVr_EX","data":{"id":"4801879"}},{"id":"as-f2kg3s","data":{"id":"4801881"}}]}'

response = requests.post('https://www.dns-shop.ru/ajax-state/product-buy/', cookies=cookies, headers=headers, data=data).json()
print(response)
products_ids = response.get("body")

with open("1_products_ids.json", 'w') as file:
    json.dump(products_ids, file, indent=4, ensure_ascii=False)

#print(response.get("body").get("products"))
