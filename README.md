# SQLModel and FastAPI example

Illustrating the fundamentals using Models with Relationships, as demonstrated in the guide: https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/

This to demonstrates retrieving the entire hierarchical structure and data from all levels. 

Relationships() is defined to achieve this:
```
class Team(TeamBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  heroes: List["Hero"] = Relationship(back_populates="team")

class Hero(HeroBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  team: Optional[Team] = Relationship(back_populates="heroes")
```
It is accomplished through a List in TeamRead and an attribute in these class definitions:
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

The implementation for a http-response/REST:
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

This solution shows the simplicity and strengths of SQLModel, pydantic and SQLAlchemy together.

## To start: 
`uvicorn.exe hero:app`

## To view API docs:
http://localhost:8000/docs

