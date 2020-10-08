import math
import requests
import random
from bs4 import BeautifulSoup

no_results = "Wow, 10 billion movies, but nothing that matched your search..."

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.118'
}


def RepresentsFloat(s):
    try:
        float(s)
        return True
    except:
        return False


def imdbFunc(rating, genres, top_or_bottom, year):
    def get_random_number():
        return random.sample(range(2, 5), 1)[0]

    def get_top_or_buttom(value: str):
        url = "https://www.imdb.com/chart/"

        if value == "top":
            url = url + "top?ref_=tt_awd"
        else:
            url = url + "bottom"

        names = []

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        movie_containers = soup.find_all('td', class_='titleColumn')

        for container in movie_containers:
            # the name
            names.append(container.a.text + " " + container.span.text)

        return random.sample(names, k=get_random_number())

    def imbd(r: str, genre: str, y: str, over: bool):
        url = "https://www.imdb.com/search/title/?title_type=feature&release_date&user_rating&num_votes=5000," \
              "&genres&sort=alpha,asc"

        if r is not None and RepresentsFloat(r):
            rate = str(r)
            if over:
                rate = rate + ","
            url = url.replace("user_rating", "user_rating=" + rate)
        else:
            url = url.replace("&user_rating", "")

        formatted_genre = genre.split(' ')

        fg = ''
        for g in formatted_genre:
            fg = fg + g + ","
        url = url.replace("genres", "genres=" + fg)

        if y is not None and RepresentsFloat(y):
            url = url.replace("release_date", "release_date=" + y + '-01-01,' + y + '-12-31')
        elif y is not None and RepresentsFloat(y.split('*')[0]) and 100 <= float(y.split('*')[0]) <= 999:
            url = url.replace("release_date", "release_date=" + y.split('*')[0] + '0-01-01,' + y.split('*')[0] + '9-12-31')
            url = url.replace("&num_votes=5000", "&num_votes=10000")
        else:
            url = url.replace("&release_date", "")

        print(url)
        selected_pages = get_page(url)

        if selected_pages == no_results:
            return no_results

        names = []

        for page in selected_pages:
            r = requests.get(page, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            movie_containers = soup.find_all('div', class_='lister-item mode-advanced')

            for container in movie_containers:
                # the name
                name = container.h3.a.text + " " + container.h3.find_all('span', class_='lister-item-year text-muted '
                                                                                        'unbold')[0].text
                names.append(name)
        if len(names) >= 5:
            return random.sample(names, k=get_random_number())
        else:
            return names

    def get_page(murl: str):
        ourl = murl

        r = requests.get(ourl, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        pages = soup.find_all('div', class_='desc')
        hc = pages[0].span
        num_of_titles = str(hc).split('>')
        num_str = num_of_titles[1].split('t')

        num_str[0] = num_str[0].replace(',', '')
        print(num_str)

        if RepresentsFloat(num_str[0]):
            num = float(num_str[0])
        elif RepresentsFloat(num_str[0][7:]):
            num = float(num_str[0][7:])
        else:
            return no_results

        num_of_pages = math.ceil(num / 50)

        nurl = murl + "&start&ref_=adv_nxt"
        url_list = []

        for i in range(num_of_pages):
            if i + 1 == 1:
                url_list.append(ourl)
            else:
                start_title_num = i * 50 + 1
                nurl = nurl.replace("start", "start=" + str(start_title_num))
                url_list.append(nurl)

        return url_list

    converted_string = ', '
    if genres is None:
        temp = get_top_or_buttom(value=top_or_bottom)
        if type(temp) == list:
            return converted_string.join(temp)
        else:
            return temp
    else:
        if RepresentsFloat(rating) and 1 <= float(rating) <= 10:
            temp = imbd(r=rating, genre=genres, y=year, over=False)
            if type(temp) == list:
                return converted_string.join(temp)
            else:
                return temp
        elif (RepresentsFloat(rating) and 1000 <= float(rating) <= 3000) or (RepresentsFloat(rating.split('*')[0]) and 100 <= float(rating.split('*')[0]) <= 999):
            temp = imbd(r=year, genre=genres, y=rating, over=False)
            if type(temp) == list:
                return converted_string.join(temp)
            else:
                return temp
        elif RepresentsFloat(rating.split('*')[0]) and 1 <= float(rating.split('*')[0]) <= 10:
            temp = imbd(r=rating.split('*')[0], genre=genres, y=year, over=True)
            if type(temp) == list:
                return converted_string.join(temp)
            else:
                return temp
        else:
            return "Rating or Year is Invalid!"
