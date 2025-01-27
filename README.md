# NAVER Cafe Crawler

NAVER Cafe Crawler using pandas, tqdm, Selenium, BeautifulSoup4

> [!CAUTION]  
> This crawler was created for educational and training purposes related to data analysis.  
> Users bear full legal responsibility for any use of this crawler.

## Requirement

- pandas
- tqdm
- Selenium
- BeautifulSoup4

Install them using pip.

```shell
pip install pandas tqdm selenium beautifulsoup4
```

## Configuring Config.py

Set your NAVER ID and password.

```python
user_id = ''
user_pw = ''
```

Specify the name and ID of the NAVER Cafe you want to crawl.

```python
cafe_name = ''
cafe_id = 0
```

## Running Prepare.py

Specify the menu ID of the NAVER Cafe and the number of pages to collect.  
> For example, if you enter `15`, it will crawl from page 1 to page 15.   
> `(Menu ID, Page number to collect)`

```python
menu_id_page = [
    (100, 15),
]
```

Run `Prepare.py` to generate a file named `[Menu ID]_link.csv`, which contains the links to be crawled.

```python
python3 Prepare.py
```

## Running Crawling.py

Provide the list of `[Menu ID]_link.csv` files to crawl.

```python
file_name_list = [
    ('100_link.csv'),
]
```

Run `Crawling.py` to perform crawling.  
It will save:
- Post contents in `[Menu ID]_content.csv`
- Comments in `[Menu ID]_comment.csv`

```python
python3 Crawling.py
```
