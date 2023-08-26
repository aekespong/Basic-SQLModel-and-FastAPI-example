
from typing import List, Optional

from fastapi import Depends
from sqlmodel import Field, Relationship, Session, SQLModel


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    team: Optional[Team] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int
    team: Optional["Team"]


class HeroCreate(HeroBase):
    pass


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None


class TeamRead(TeamBase):
    id: int
    heroes: List["Hero"]


# TeamRead.update_forward_refs()  # Nödvänding för att team.heroes ska ha en referen till objektet Hero och inte till Any
    

def create_heroes(engine):
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            team=team_z_force,
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team=team_preventers
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", team=team_preventers
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond)
        print("Deadpond team:", hero_deadpond.team)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man team:", hero_rusty_man.team)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy team:", hero_spider_boy.team)