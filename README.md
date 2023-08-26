# SQLModel-example

Illustrating the fundamentals using Models with Relationships in FastAPI, as demonstrated in the guide: https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/

This particular instance serves to demonstrate the process of comprehensively retrieving and visualizing the entire hierarchical structure. In this case Teams encompass Heroes in a one-to-many relationship, while Heroes are associated with teams in a many-to-one capacity.

A crucial insight lies in appending a List to both TeamRead and HeroRead, a nuance that isn't covered in the documentation's example but is covered with these class definitions:

```
class TeamRead(TeamBase): 
  id: int 
  heroes: List["Hero"]

class HeroRead(HeroBase): 
  id: int 
  team: Optional["Team"]
```

The order of the data object classes is essential. Sometimes TeamRead.update_forward_refs() is needed to make the references work.

In http://localhost:8000/docs TeamRead and HeroRead respectively have correct field for the sub items. 

This is the implemented in this way:
```
@app.get("/team/{team_id}", response_model=TeamRead)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
  team = session.get(Team, team_id)
  if not team:
    raise HTTPException(status_code=404, detail="Team not found")
  return team
```
Note that retrieving the whole hierarchical structure of Teams and Heroes is achieved with only one line of code: 

`team = session.get(Team, team_id)`

Relationships() is used to achieve this and they are defined as:
```
class Team(TeamBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(HeroBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  team: Optional[Team] = Relationship(back_populates="heroes")
```
This solution shows the simplicity and strengths of SQLModel, pydantic and SQLAlchemy together.

## To start: 
`uvicorn.exe hero:app`

## To view swagger docs:
http://localhost:8000/docs

