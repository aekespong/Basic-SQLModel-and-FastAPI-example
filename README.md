# SQLModel-example
Basic example based on Models with Relationships in FastAPI: https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/

Teams includes Heroes (one-to-many) and Heroes includes teams (many-to-one) and this example shows how to read and get the whole structure and all levels.

The key is to add List to the TeamRead and HeroRead respectivly which is not part of the sample in the docs.

`class TeamRead(TeamBase): id: int heroes: List["Hero"]`

`class HeroRead(HeroBase): id: int team: Optional["Team"]`

The order of the data object classes is essential. Sometimes TeamRead.update_forward_refs() is needed to make the references work.

Have a look at the /docs and TeamRead and HeroRead respectively to verify that both have correct detailed descriptions of every field.
```
@app.get("/team/{team_id}", response_model=TeamRead)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
  team = session.get(Team, team_id)
  if not team:
    raise HTTPException(status_code=404, detail="Team not found")
  return team
```
The code for retrieving the whole structure of Teams and Heroes is achieved with only one line of code: team = session.get(Team, team_id) It is all thanks to the Relationships defined as:

class Team(TeamBase, table=True): id: Optional[int] = Field(default=None, primary_key=True) heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(HeroBase, table=True): id: Optional[int] = Field(default=None, primary_key=True) team: Optional[Team] = Relationship(back_populates="heroes")

This solution shows the simplicity and strengths of SQLModel, pydantic and SQLAlchemy together.

New File at / · aekespong/SQLModel-example
