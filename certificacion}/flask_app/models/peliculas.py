from flask_app.config.mysqlconnection import connectToMySQL 


class Movie:
    def __init__(self, data):
        self.id = data['id']
        self.nombre_pelicula = data['nombre_pelicula']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO peliculas (nombre_pelicula, director, fecha_estreno, sinopsis) VALUES (%(nombre_pelicula)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s);"
        return connectToMySQL('esquema_tacos').query_db(query, data)

