from perfect_gym_api.models.settings import RequestHeaders


def generate_headers(headers: RequestHeaders):
    result = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pl-PL,pl;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': headers.cookie,
        'Cp-Lang': 'pl',
        'Cp-Mode': 'desktop',
        'Host': headers.host,
        'Origin': headers.origin,
        'Pragma': 'no-cache',
        'Referer': headers.referer,
        'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Gpc': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Hash': '#/Login',
        'X-Requested-With': 'XMLHttpRequest'
    }
    return result
