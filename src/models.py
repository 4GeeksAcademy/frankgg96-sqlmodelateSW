from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model): 
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    subscription_date: Mapped[str] = mapped_column(String(100))
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    climate: Mapped[str] = mapped_column(String(100))
    population: Mapped[int] = mapped_column(Integer)

class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    gender: Mapped[str] = mapped_column(String(100))
    eye_color: Mapped[str] = mapped_column(String(100))

    def serialize(self):
        return {
            "id":self.id, 
            "name":self.name,
            "gender":self.gender,
            "eye_color":self.eye_color 
            
        }
        
                                         
class Favorite(db.Model): 
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=True)
    user: Mapped["User"] = relationship(back_populates="favorites")        

