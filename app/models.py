from sqlmodel import Field, Relationship, SQLModel


class Data(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp : str
    visitors_count : int
    max_capacity : int

    facility_id : int = Field(default=None, foreign_key="facility.id")
    facility : "Facility" = Relationship(back_populates="data_readings")

class Facility(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    organization_unit : int
    name: str
    type: str

    data_readings: list[Data] = Relationship(back_populates="facility")

class Settings(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    external_api_timeout : int
    fetch_interval : int
