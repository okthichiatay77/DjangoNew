import requests
from bs4 import BeautifulSoup


def handle_total(domain):
    data = requests.get('https://' + domain)
    soup = BeautifulSoup(data.content, 'html.parser')
    url_img = soup.find('img', attrs={'class': 'themeforbirthday'})

    canonical = handle_conanical(soup)
    title = handle_title(soup)
    heading = handle_heading(soup)
    desc = handle_meta_description(soup)
    iframe = handle_iframe(soup)

    return [url_img, title, canonical, desc, heading, iframe]


def html_version(soup):
    ...

def handle_heading(soup):
    list_h1 = soup.find_all("h1")
    if len(list_h1) == 0:
        result = 'Trang web của bạn không có thẻ h1.'
    elif len(list_h1) > 1:
        result = 'Trang web của bạn có nhiều hơn một thẻ h1 để tối ưu bạn nên sử dụng một thẻ h1.'
    else:
        result = 'Pass'

    return result

def handle_title(soup):

    title = soup.find_all('title')
    if title:
        if len(title) > 1:
            result = 'Trang web của bạn có nhiều hơn một thẻ meta title'
        elif len(title) == 0:
            result = 'Trang web của bạn không có thẻ meta title'
        else:
            content = title[0].get_text()
            if len(content) > 100:
                result = 'Nội dung của the meta title dài hơn 100 ký tự vui lòng tối ưu hóa lại'
            else:
                result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ title'

    return result

def handle_conanical(soup):

    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical:
        result = 'Hoàn hảo trang web của bạn đã có thẻ canonical.'
    else:
        result = 'Trang web của bạn không có thẻ Canonical'

    return result

def handle_meta_description(soup):
    meta_des = soup.find_all('meta', attrs= {'name': 'description'})

    if len(meta_des) > 1:
        result = 'Trang web của bạn có nhiều hơn một thẻ meta description.'
    elif len(meta_des) == 0:
        result = 'Trang web của bạn không có thẻ meta description.'
    else:
        result = 'Pass'
    return result

def handle_iframe(soup):
    list_iframe = soup.find_all('iframe')

    if len(list_iframe) > 0:
        result = 'Trang web của bạn có thẻ iframe hãy cẩn thận khi sử dụng chúng'
    else:
        result = 'Pass'

    return result

def meta_robots(soup):
    result = ''

    return result

def meta_revisit_after(soup):
    result = ''

    return result


def content_language(soup):
    result = ''

    return result

def content_type(soup):
    result = ''

    return result

def meta_viewport(soup):
    result = ''

    return result

def favicon(soup):
    result = ''

    return result


def image_alt(soup):
    result = ''

    return result

def check_nofollow(soup):
    result = ''

    return result

def handle_sitemap(soup):
    result = ''

    return result

def image_size(soup):
    result = ''

    return result

def page_loading_speed(soup):
    result = ''

    return result

def AMP(soup):
    result = ''

    return result

def index(soup):
    result = ''

    return result

def tag_name_not_in_html5(soup):
    result = ''

    return result