
import datetime

content = [
    {
        "id": 0,
        "title": "Test Book 1",
        "isbn": "9781234567897",
        "published_date": datetime.date(2019, 4, 13).isoformat(),
        "authors": [
            "Rea Horne",
            "Cristiano Searle"
        ]
    },
    {
        "id": 1,
        "title": "Test Book 2",
        "isbn": "9781234562397",
        "published_date": datetime.date(2018, 4, 13).isoformat(),
        "authors": [
            "Abbey Sullivan",
            "Paige Parry",
            "Tahir Frey",
        ]
    },
    {
        "id": 2,
        "title": "Test Book 3",
        "isbn": "9781245567897",
        "published_date": datetime.date(2017, 4, 10).isoformat(),
        "authors": [
            "Lavinia Winters",
            "Ella-Louise Estrada",
            "Layla Frye",
            "Colm Small",
        ]
    },
]


class BookShelf:

    def __init__(self):
        self.books = content

    def get_all(self):
        return self.books

    def get(self, id):
        ret = list(filter(lambda item: item['id'] == id, self.books))
        if ret:
            ret = ret[0]
        return ret

    def create(self, data):
        self.books.append(data)

    def update(self, id, data):
        for d in self.books:
            if d['id'] == id:
                d.update(data)
                break
        else:
            raise KeyError

    def delete(self, id):
        for d in self.books:
            if d['id'] == id:
                self.books.remove(d)
                break
        else:
            raise KeyError
