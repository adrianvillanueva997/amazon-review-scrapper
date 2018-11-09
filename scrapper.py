import requests
from bs4 import BeautifulSoup
import time


def make_request(url):
    """
    Recieves an url and returns the raw html code of a webpage.
    :returns html: str
    :argument url: str
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = requests.get(url=url, headers=headers)
    print(f'[INFO] Request made to: {url} with response: {request}')
    html = request.content

    return html


def get_div_blocks(html):
    """
    Recieves the raw html code and returns a list with the div class blocks that we want.
    :returns div_class_blocks: list
    :argument url: str
    """
    soup = BeautifulSoup(html, 'html.parser')
    div_class_blocks = soup.findAll("div", class_='a-section review')
    return div_class_blocks


def check_limit(html):
    soup = BeautifulSoup(html, 'html.parser')
    limit = soup.find('div', {'class': 'a-section a-spacing-top-large a-text-center no-reviews-section'})
    limit = str(limit).replace(
        '<div class="a-section a-spacing-top-large a-text-center no-reviews-section"><span class="a-size-medium">', '')
    if len(limit) == 4:
        return True
    else:
        return False


def filter_data(div_blocks):
    """
    Recieves a list of div classes and filters the reviews by the rating score, returns a dictionary with 3 lists, one for each kind of review.
    :returns datos : dict
    :argument div_blocks: list
    """
    # malas: 1-2
    # neutras: 3
    # buenas: 4-5
    datos = {
        'malas': [],
        'neutras': [],
        'buenas': []
    }
    for block in div_blocks:
        soup = BeautifulSoup(str(block), 'html.parser')
        rating = soup.find('span', {'class': 'a-icon-alt'})
        rating = str(rating).replace('<span class="a-icon-alt">', '')
        rating = rating.replace('</span>', '')
        rating = rating.replace(',0 de 5 estrellas', '')

        review = soup.find('span', {'class': 'a-size-base review-text'})
        review = str(review).replace('<span class="a-size-base review-text" data-hook="review-body">', '')
        review = review.replace('<br/>', '')
        review = review.replace('</span>', '')
        rating = int(rating)

        if rating == 1 or rating == 2:
            datos['malas'].append(review)
        elif rating == 3:
            datos['neutras'].append(review)
        elif rating == 4 or rating == 5:
            datos['buenas'].append(review)

    return datos


def export_reviews(path, file_name, index, review):
    """
    Exports the review.
    :argument path,file_name,index,review: str
    """
    with open(path + str(index) + '_' + file_name + '.txt', 'w', encoding='utf-8') as file:
        file.write(review)


if __name__ == '__main__':
    urls = [
        'https://www.amazon.es/Apple-iPhone-Espacial-Smartphone-Reacondicionado/product-reviews/B01L9KXU7O/',
    ]
    data = {
        'malas': [],
        'neutras': [],
        'buenas': []
    }
    for url in urls:
        num_page = 1
        max = 2
        while num_page < max:
            html = make_request(url + 'cm_cr_arp_d_paging_btm_' + str(num_page) + '?pageNumber=' + str(num_page))
            blocks = get_div_blocks(html)
            if check_limit(html) == True:
                filtered_data = filter_data(blocks)
                for malas in filtered_data['malas']:
                    data['malas'].append(malas)
                for neutras in filtered_data['neutras']:
                    data['neutras'].append(neutras)
                for buenas in filtered_data['buenas']:
                    data['buenas'].append(buenas)
                num_page += 1
                max += 1
            else:
                num_page = max

    mala_total = len(data['malas'])
    neutra_total = len(data['neutras'])
    buena_total = len(data['buenas'])
    print('malas:', str(mala_total))
    print('neutras: ', str(neutra_total))
    print('buenas: ', str(buena_total))
    print('total: ', str(mala_total + neutra_total + buena_total))

    print('[INFO] Exporting bad reviews')
    filename = 'mala'
    index = 1
    path = r'/home/xiao/Documents/dataset-computacion/malas/'
    for review_mala in data['malas']:
        export_reviews(path, filename, str(index), review_mala)
        index += 1

    filename = 'buena'
    index = 1
    path = r'/home/xiao/Documents/dataset-computacion/buenas/'
    print('[INFO] Exporting good reviews')
    for review_mala in data['buenas']:
        export_reviews(path, filename, str(index), review_mala)
        index += 1

    filename = 'neutra'
    index = 1
    path = r'/home/xiao/Documents/dataset-computacion/neutras/'
    print('[INFO] Exporting neutral reviews')
    for review_mala in data['neutras']:
        export_reviews(path, filename, str(index), review_mala)
        index += 1
