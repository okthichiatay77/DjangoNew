from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def handle_total(domain):
    data = requests.get(domain)
    soup = BeautifulSoup(data.content.lower(), 'html.parser')

    url_img = soup.find_all('link')
    for img in url_img:
        if 'icon' in img['rel']:
            url_img = img['href']
            break

    if 'http' not in url_img:
        url_img = domain + url_img

    title = handle_title(soup)
    desc = handle_meta_description(soup)
    canonical = handle_conanical(soup)
    robot = meta_robots(soup)
    revisit_after = meta_revisit_after(soup)
    content_lang = content_language(soup)
    meta_content_type = content_type(soup)
    viewport = meta_viewport(soup)

    iframe = handle_iframe(soup)

    heading = handle_heading(soup)
    list_ex = link_external(domain, soup)
    favicon_check = favicon(soup)
    check_sitemap = handle_sitemap(domain)

    return [
        url_img,
        title,
        desc,
        canonical,
        robot,
        revisit_after,
        content_lang,
        meta_content_type,
        viewport,

        heading,
        iframe,
        list_ex,
        favicon_check,
        check_sitemap,
    ]


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
        result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ Canonical'

    return result


def handle_meta_description(soup):
    meta_des = soup.find_all('meta', attrs={'name': 'description'})

    if len(meta_des) > 1:
        result = 'Trang web của bạn có nhiều hơn một thẻ meta description.'
    elif len(meta_des) == 0:
        result = 'Trang web của bạn không có thẻ meta description.'
    else:
        result = 'Pass'
    return result


def meta_robots(soup):
    result = ''
    check = soup.find_all('meta', attrs={'name': 'robots'})
    if check:
        if len(check) > 1:
            result = 'Trang web của bạn có thẻ meta robots trùng lặp'
        else:
            result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ meta robots'

    return result


def meta_revisit_after(soup):
    result = ''
    check = soup.find_all('meta', attrs={'name': 'revisit-after'})
    if check:
        if len(check) > 1:
            result = 'Trang web của bạn có thẻ meta revisit-after trùng lặp'
        else:
            result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ meta revisit-after'

    return result


def content_language(soup):
    result = ''
    check = soup.find_all('meta', attrs={'name': 'content-language'})
    if check:
        if len(check) > 1:
            result = 'Trang web của bạn có thẻ meta content-language trùng lặp'
        else:
            result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ meta content-language'

    return result


def content_type(soup):
    result = ''

    check = soup.find_all('meta', attrs={'http-equiv': 'content-type'})
    if check:
        if len(check) > 1:
            result = 'Trang web của bạn có thẻ meta content-type trùng lặp'
        else:
            result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ meta content-type'

    return result


def meta_viewport(soup):

    check = soup.find_all('meta', attrs={'name': 'viewport'})
    if check:
        if len(check) > 1:
            result = 'Trang web của bạn có thẻ meta viewport trùng lặp'
        else:
            result = 'Pass'
    else:
        result = 'Trang web của bạn không có thẻ meta viewport'

    return result


def favicon(soup):
    result = ''
    check_icon = 0
    for link in soup.head.find_all('link'):
        if 'icon' in link['rel']:
            check_icon = 1
            break

    if check_icon == 0:
        result = 'Trang web của bạn không có favicon'
    elif check_icon == 1:
        result = 'Pass'

    return result


def image_alt(soup):
    result = ''

    return result


def check_nofollow(soup):
    result = ''

    return result


def handle_sitemap(domain):
    status_code = requests.get(domain + '/sitemap.xml').status_code
    if status_code != 200:
        result = 'Trang web của bạn không có file sitemap.xml'
    else:
        result = 'Pass'

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


def link_external(domain, soup):
    domain_netloc = urlparse(domain).netloc
    list_ex = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if ('http' in href) and (domain_netloc not in urlparse(href).netloc):
            list_ex.append(href)

    return list_ex


def handle_iframe(soup):
    list_iframe = soup.find_all('iframe')

    if len(list_iframe) > 0:
        result = 'Trang web của bạn có thẻ iframe hãy cẩn thận khi sử dụng chúng'
    else:
        result = 'Pass'

    return result
