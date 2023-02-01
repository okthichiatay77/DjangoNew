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
    img_alt = image_alt(soup)

    context = {'url_img': url_img, 'canonical': canonical,
               'title': title, 'heading': heading,
               'desc': desc, 'r_iframe': iframe,
               'list_link_external': list_ex, 'favicon': favicon_check,
               'robot': robot,
               'revisit_after': revisit_after, 'content_language': content_lang,
               'meta_content_type': meta_content_type, 'viewport': viewport,
               'check_sitemap': check_sitemap, 'image_alt': img_alt}
    return context



def handle_heading(soup):
    list_h1 = soup.find_all("h1")
    if len(list_h1) == 0:
        msg = 'Trang web của bạn không có thẻ h1.'
        status = 'Error'
    elif len(list_h1) > 1:
        msg = 'Trang web của bạn có nhiều hơn một thẻ h1 để tối ưu bạn nên sử dụng một thẻ h1.'
        status = 'Warning'
    else:
        msg = 'Tốt. Trang web của bạn chỉ có một thẻ h1.'
        status = 'Pass'

    result = [status, msg]

    return result


def handle_title(soup):
    title = soup.find_all('title')
    if title:
        if len(title) > 1:
            msg = 'Trang web của bạn có nhiều hơn một thẻ meta title'
            status = 'Warning'
        elif len(title) == 0:
            msg = 'Trang web của bạn không có thẻ meta title'
            status = 'Error'
        else:
            content = title[0].get_text()
            if len(content) > 100:
                msg = 'Nội dung của the meta title dài hơn 100 ký tự. Vui lòng kiểm tra lại'
                status = 'Warning'
            else:
                msg = 'Tốt. Trang web của bạn thẻ title đúng yêu cầu'
                status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ title'
        status = 'Error'

    result = [status, msg]
    return result


def handle_conanical(soup):
    canonical = soup.find('link', attrs={'rel': 'canonical'})
    if canonical:
        msg = 'Tốt. Trang của bạn có thẻ meta conanical'
        status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ meta canonical'
        status = 'Warning'

    result = [status, msg]
    return result


def handle_meta_description(soup):
    meta_des = soup.find_all('meta', attrs={'name': 'description'})

    if len(meta_des) > 1:
        msg = 'Trang web của bạn có nhiều hơn một thẻ meta description.'
        status = 'Warning'
    elif len(meta_des) == 0:
        msg = 'Trang web của bạn không có thẻ meta description.'
        status = 'Error'
    else:
        msg = 'Tốt. Trang web của bạn có thẻ meta description đúng yêu cầu'
        status = 'Pass'

    result = [status, msg]
    return result


def meta_robots(soup):
    check = soup.find_all('meta', attrs={'name': 'robots'})
    if check:
        if len(check) > 1:
            msg = 'Trang web của bạn có thẻ meta robots trùng lặp'
            status = 'Warning'
        else:
            msg = 'Tốt. Trang web của bạn có thẻ meta robots theo yêu cầu'
            status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ meta robots'
        status = 'Error'

    result = [status, msg]
    return result


def meta_revisit_after(soup):
    check = soup.find_all('meta', attrs={'name': 'revisit-after'})
    if check:
        if len(check) > 1:
            msg = 'Trang web của bạn có thẻ meta revisit-after trùng lặp'
            status = 'Warning'
        else:
            msg = 'Tốt. Trang web của bạn có thẻ đúng yêu cầu'
            status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ meta revisit-after'
        status = 'Error'

    result = [status, msg]
    return result


def content_language(soup):
    check = soup.find_all('meta', attrs={'name': 'content-language'})
    if check:
        if len(check) > 1:
            msg = 'Trang web của bạn có thẻ meta content-language trùng lặp'
            status = 'Warning'
        else:
            msg = 'Tốt. Trang web của bạn có thẻ content-language'
            status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ meta content-language'
        status = 'Error'

    result = [status, msg]
    return result


def content_type(soup):
    check = soup.find_all('meta', attrs={'http-equiv': 'content-type'})
    if check:
        if len(check) > 1:
            msg = 'Trang web của bạn có thẻ meta content-type trùng lặp'
            status = 'Warning'
        else:
            msg = 'Tốt. Trang web của bạn có thẻ content-type'
            status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ meta content-type'
        status = 'Error'

    result = [status, msg]
    return result


def meta_viewport(soup):
    check = soup.find_all('meta', attrs={'name': 'viewport'})
    if check:
        if len(check) > 1:
            msg = 'Trang web của bạn có thẻ meta viewport trùng lặp'
            status = 'Warning'
        else:
            msg = 'Tốt. Trang web của bạn có thẻ viewport'
            status = 'Pass'
    else:
        msg = 'Trang web của bạn không có thẻ meta viewport'
        status = 'Error'

    result = [status, msg]
    return result


def favicon(soup):
    check_icon = 0
    for link in soup.head.find_all('link'):
        if 'icon' in link['rel']:
            check_icon = 1
            break

    if check_icon == 0:
        msg = 'Trang web của bạn không có favicon'
        status = 'Error'
    else:
        msg = 'Tốt. Trang web của bạn có icon'
        status = 'Pass'

    result = [status, msg]
    return result


def image_alt(soup):
    check = 0
    list_img = soup.find_all('img', src=True)
    for img in list_img:
        try:
            img['alt']
        except:
            check += 1

    if check > 0:
        msg = 'Trang web của bạn có ' + str(check) + ' thẻ không có thuộc tính alt'
        status = 'Warning'
    else:
        msg = 'Tốt trang của bạn tất cả thẻ img có thuộc tính alt'
        status = 'Pass'

    result = [status, msg]

    return result


def check_nofollow(soup):
    result = ''

    return result


def handle_sitemap(domain):
    if domain[-1] == '/':
        status_code = requests.get(domain + 'sitemap.xml').status_code
    else:
        status_code = requests.get(domain + '/sitemap.xml').status_code
    if status_code != 200:
        msg = 'Trang web của bạn không có file sitemap.xml'
        status = 'Error'
    else:
        msg = 'Tốt. Trang của bạn có file sitemap'
        status = 'Pass'

    result = [status, msg]
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
