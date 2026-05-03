from pprint import pprint
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from pprint import pprint
from utils import save_json
url = 'https://old.reddit.com/search?q=marketing+agencey'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
html  = requests.get(url, headers=headers)




soup = BeautifulSoup(html.text, "html.parser")

contents_div = soup.find_all("div", class_= "contents")[-1]

posts = []
for content_div in tqdm(contents_div):
    search_result_header = content_div.find("header", class_="search-result-header")
    print(search_result_header)
    a_tag = search_result_header.find("a")
    title = a_tag.text
    post_url = a_tag["href"]

    search_expando = content_div.find("div", class_ ="search-expando collapsed")
    post_text = None
    if search_expando:
        post_text = content_div.find("div", class_="search-result-body").text


    search_result_meta = content_div.find("div", class_="search-result-meta")
    search_score = search_result_meta.find("span", class_= "search-score").text
    num_comments = search_result_meta.find("a").text

    time_metadata = search_result_meta.find("span", class_="search-time").find("time")
    search_time = time_metadata["title"]

    how_long_ago= time_metadata.text

    post_author = search_result_meta.find("span", class_="search-author").find("a").text

    posts.append(
        {
            "title": title, 
            "post_url": post_url, 
            "post_text": post_text, 
            "search_score": search_score, 
            "num_comments":num_comments,
            "search_time":search_time, 
            "how_long_ago":how_long_ago, 
            "post_author":post_author 
        }
    )

pprint(posts)
save_json(posts)