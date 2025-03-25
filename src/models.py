from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Personajes(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    genero: Mapped[str] = mapped_column(nullable=False)
    favoritos = relationship("Favoritos", back_populates="personajes")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genero": self.genero,
        }

class Planetas(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[str] = mapped_column(nullable=False)
    favoritos = relationship("Favoritos", back_populates="planetas")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
        }

class Usuarios(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    mail: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favoritos = relationship("Favoritos", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
        }

class Favoritos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    user = relationship("Usuarios", back_populates="favoritos")
    personajes_id: Mapped[int] = mapped_column(ForeignKey("personajes.id"))
    personajes = relationship("Personajes", back_populates="favoritos")
    planetas_id: Mapped[int] = mapped_column(ForeignKey("planetas.id"))
    planetas = relationship("Planetas", back_populates="favoritos")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personajes_id": self.personajes_id,
            "planetas_id": self.planetas_id,
        }
