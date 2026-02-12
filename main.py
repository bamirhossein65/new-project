import requests
from pydantic import BaseModel
import csv

file_name = "books.csv"


class BookModel(BaseModel):
    title:str
    publish_year:int

url = "https://openlibrary.org/search.json?q=python&limit=50"
response = requests.get(url)
data = response.json()

raw_books = data.get("docs",[])

books = []
after_2000_year = []
for i in raw_books:
    book = BookModel(
        title = i.get("title"),
        publish_year = i.get("first_publish_year")
    )
    books.append(book)

for i in books:
    if i.publish_year >= 2000:
        after_2000_year.append(i)

with open(file_name, mode="w", encoding= "utf-8",newline="") as file:
    fieldnames = ["title", "publish_year"]

    writer = csv.DictWriter(file,fieldnames=fieldnames,)

    writer.writeheader()

    for i in after_2000_year:
        writer.writerow(i.model_dump())

