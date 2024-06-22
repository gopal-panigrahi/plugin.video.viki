from codequick.utils import urljoin_partial

# URLs
CONTENT_BASE_URL = "https://api.viki.io/v4/"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

BASE_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en",
    "Priority": "u=1, i",
    "Referer": "https://www.google.com/",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": USER_AGENT,
    "X-Client-User-Agent": USER_AGENT,
    "X-Viki-App-Ver": "14.16.2",
}

url_constructor = urljoin_partial(CONTENT_BASE_URL)

MAIN_MENU = [
    ("Korean", "kr", "korean.png"),
    ("Mainland China", "cn", "china.png"),
    ("Japan", "jp", "japan.png"),
    ("Taiwan", "tw", "taiwan.png"),
    ("Thailand", "th", "thailand.png"),
    ("Others", "vn", "others.png"),
]

URLS = {
    "CONTAINER": "containers.json",
    "EPISODES": "series/{id}/episodes.json",
    "MOVIE": "films/{id}/movies.json",
    "VIDEO": "https://www.viki.com/api/videos/{id}",
}

GENRES = {
    "1g": "Action",
    "2g": "Animation",
    "6g": "Comedy",
    "7g": "Crime & Mystery",
    "8g": "Documentary",
    "9g": "Drama",
    "10g": "Entertainment",
    "12g": "Supernatural",
    "17g": "Music",
    "18g": "Romantic Comedy",
    "19g": "Fantasy",
    "20g": "Sports",
    "24g": "Family & Kids",
    "25g": "Costume & Period",
    "26g": "Thriller & Suspense",
    "1037g": "Historical",
    "1038g": "Idol Drama",
    "1040g": "Medical Drama",
    "1041g": "Melodrama",
    "1044g": "Variety Show",
    "1045g": "Web Drama",
    "1047g": "Short Films",
    "1050g": "War",
    "1055g": "Travel",
    "1063g": "Horror",
    "1064g": "Sci-Fi",
    "1067g": "BL",
    "1068g": "Romance",
    "1069g": "Awards",
    "1070g": "Performance",
    "1071g": "GL",
    "1072g": "Adventure",
}
