def random():
    import requests
    import re

    page: requests.Response = requests.get("https://risibank.fr/stickers/hasard")
    content: str = page.text.replace('\n', '')

    regex: re.Match = re.search(
        r'<tr><td>Lien direct</td><td><b><a target=\"_blank\" rel=\"nofollow\" href=\"([^\"]*)\">', content)
    res: str = regex.groups()[0]
    return res
