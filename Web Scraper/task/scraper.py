from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
import string
import os

pages = int(input())
type_of_article = input()
signs = dict.fromkeys(string.punctuation)
# signs["‘"] = None
# signs["—"] = None
# signs["’"] = None
signs = str.maketrans(signs)
articles_signatures = [{"class": "c-article-body u-clearfix"}, {"class": "article-item__body"}]
for page in range(1, pages + 1):
    url = "https://www.nature.com/nature/articles"
    r = requests.get(url, params={"page": page}, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r:
        soup = BeautifulSoup(r.content, "html5lib")
        articles = soup.find_all("article")
        result = []
        if not os.path.isdir(f'Page_{page}'):
            os.mkdir(f'Page_{page}')
        for article in articles:
            is_article = article.find("span", attrs={"data-test": "article.type"}).span.text
            if is_article == type_of_article:
                article_name = article.find("a", attrs={"data-track-action": "view article"})
                article_href = article_name["href"]

                article_name = article_name.text.translate(signs).replace(" ", "_")
                result.append(f'{article_name}.txt')
                r = requests.get(urljoin(url, article_href), headers={'Accept-Language': 'en-US,en;q=0.5'})
                if r:
                    # content_of_article = r.content.replace(b"<i>", b" ")
                    # content_of_article = content_of_article.replace(b"</i>", b" ")
                    # content_of_article = re.sub(b' +', b' ', content_of_article)
                    soup_for_article = BeautifulSoup(r.content, "html.parser")
                    #  print(soup_for_article.prettify())

                    for sign in articles_signatures:
                        article_body = soup_for_article.find("div", attrs=sign)
                        if article_body is not None:
                            break
                    text_of_article = article_body.text.strip()  # get_text(strip=True)

                    with open(os.path.join(f'Page_{page}/', f'{article_name}.txt'), "wb") as out_file:
                        out_file.write(text_of_article.encode("utf-8"))

    print(f'Saved articles:\n{result}')

# print(article.prettify())
# for string in article.stripped_strings:
#     print(string)
# #     # text = article.text.split("\n")
# #     # print(article)
# print("\n_____________________\n")
#     if article.div.div.div.span.span.string == "Article":
#         print(article.div.h3.a.string)

# description = soup.find("div", attrs={'role': 'presentation', 'data-testid': 'plot-xl'})
# print(title.text)
# print(description.text)
#     if title is None or description is None:
#         print("Invalid movie page!")
#         exit()
#     print({"title": title.text, "description": description.text})
# else:
#     print("Invalid movie page!")

# page_content = requests.get(input())
# if page_content.status_code == 200:
#     with open('source.html', 'wb') as file_out:
#         file_out.write(page_content.content)
#     print("Content saved.")
# else:
#     print(f'The URL returned {page_content.status_code}')
