import requests
from bs4 import BeautifulSoup


def make_request(url):
    """
    Function that recieves an url and returns the raw html code of a webpage.
    :returns html: str
    :argument url: str
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = requests.get(url=url, headers=headers)
    print(f'[INFO] Request made to: {url} with response: {request}')
    html = request.content
    return html


def get_div_blocks(html):
    soup = BeautifulSoup(html, 'html.parser')
    div_class_blocks = soup.findAll("div", class_='a-section review')
    return div_class_blocks


def filter_data(div_blocks):
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
    with open(path + str(index) + '_' + file_name + '.txt', 'w', encoding='utf-8') as file:
        file.write(review)


if __name__ == '__main__':
    urls = [
        'https://www.amazon.es/Apple-iPhone-Plata-Smartphone-Reacondicionado/product-reviews/B01L9KWM6E/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
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
            html = make_request(url + str(num_page))
            blocks = get_div_blocks(html)
            if len(blocks) != 0:
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

    print('malas:', str(len(data['malas'])))
    print('neutras: ', str(len(data['neutras'])))
    print('buenas: ', str(len(data['buenas'])))

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
