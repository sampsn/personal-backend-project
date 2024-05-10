from sqlmodel import SQLModel

from models import Engine, Transmission, BodyStyle


class NewTrimRequest(SQLModel):
    name: str
    model: str


class NewEngineRequest(SQLModel):
    name: str
    hp: int
    tq: int
    displacement: float
    cylinders: int
    configuration: str
    redline: int
    dry_weight: int
    aspiration: str


class NewTransmissionRequest(SQLModel):
    name: str
    type: str


class NewBodyStyleRequest(SQLModel):
    name: str


class NewCarRequest(SQLModel):
    year: int
    weight: int
    length: float
    width: float
    engines: list[NewEngineRequest]
    transmissions: list[NewTransmissionRequest]
    bodystyles: list[NewBodyStyleRequest]
