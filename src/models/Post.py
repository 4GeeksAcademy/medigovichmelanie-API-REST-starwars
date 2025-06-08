from database.db import db


class Post(db.Model):
    # Aquí definimos el nombre de la tabla "Person"
    # Es opcional debiado a que usa el nombre de la clase por defecto.
    __tablename__ = "post"

    # Ten en cuenta que cada columna es también un atributo normal de primera instancia de Python.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='post')

    # El método serialize convierte el objeto en un diccionario

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
        }
