from flask import current_app

from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(Movie).get(bid)

    def get_all(self, filters):
        t = self.session.query(Movie)
        if filters.get("director_id") is not None:
            t = t.filter(Movie.director_id == filters.get("director_id"))
        if filters.get("genre_id") is not None:
            t = t.filter(Movie.genre_id == filters.get("genre_id"))
        if filters.get("year") is not None:
            t = t.filter(Movie.year == filters.get("year"))
        if filters.get("newiest") is not None:
            t = t.order_by(Movie.year)
        if filters.get("paginate") is not None:
            t = t.limit(current_app.config['ITEMS_PER_PAGE']).offset(
                current_app.config['ITEMS_PER_PAGE'] * (int(filters.get("paginate")) - 1))
        return t.all()

    def create(self, movie_d):
        ent = Movie(**movie_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        movie = self.get_one(rid)
        self.session.delete(movie)
        self.session.commit()

    def update(self, movie_d):
        movie = self.get_one(movie_d.get("id"))
        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self.session.add(movie)
        self.session.commit()
