from sqlmodel import Field, SQLModel, Relationship, create_engine, Session


class Make(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    models: list["Model"] = Relationship(back_populates="make")


class MakeResponse(SQLModel):
    name: str
    models: list["ModelResponse"]


class ModelResponse(SQLModel):
    name: str
    trims: list["Trim"]


class Model(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    make_id: int | None = Field(default=None, foreign_key="make.id")

    make: Make | None = Relationship(back_populates="models")
    trims: list["Trim"] = Relationship(back_populates="model")
    generations: list["Generation"] = Relationship(back_populates="model")


class Generation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    modelid: int | None = Field(default=None, foreign_key="model.id")

    model: Model | None = Relationship(back_populates="generations")
    chassis_codes: list["ChassisCode"] = Relationship(back_populates="generation")


class ChassisCode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    generation_id: int | None = Field(default=None, foreign_key="generation.id")

    generation: Generation | None = Relationship(back_populates="chassis_codes")
    cars: list["Car"] = Relationship(back_populates="chassis_code")


class Trim(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    modelid: int | None = Field(default=None, foreign_key="model.id")

    model: Model | None = Relationship(back_populates="trims")
    cars: list["Car"] = Relationship(back_populates="trim")


class EngineCarLink(SQLModel, table=True):
    car_id: int | None = Field(default=None, foreign_key="car.id", primary_key=True)
    engine_id: int | None = Field(
        default=None, foreign_key="engine.id", primary_key=True
    )


class TransmissionCarLink(SQLModel, table=True):
    car_id: int | None = Field(default=None, foreign_key="car.id", primary_key=True)
    transmission_id: int | None = Field(
        default=None, foreign_key="transmission.id", primary_key=True
    )


class BodyStyleCarLink(SQLModel, table=True):
    car_id: int | None = Field(default=None, foreign_key="car.id", primary_key=True)
    bodystyle_id: int | None = Field(
        default=None, foreign_key="bodystyle.id", primary_key=True
    )


class Car(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int
    trim_id: int | None = Field(default=None, foreign_key="trim.id")
    trim: Trim | None = Relationship(back_populates="cars")
    chassis_code_id: int | None = Field(default=None, foreign_key="chassiscode.id")
    chassis_code: ChassisCode | None = Relationship(back_populates="cars")
    engines: list["Engine"] = Relationship(
        back_populates="cars", link_model=EngineCarLink
    )
    transmissions: list["Transmission"] = Relationship(
        back_populates="cars", link_model=TransmissionCarLink
    )
    bodystyles: list["BodyStyle"] = Relationship(
        back_populates="cars", link_model=BodyStyleCarLink
    )
    weight: int
    length: float
    width: float


class Engine(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    hp: int
    tq: int
    aspiration: str
    # NA = Naturally Aspirated | TT = Twin Turbo | T = Turbocharged | SC-B = Supercharged w/ Blower | SC-C = Supercharged w/ Centrifugal
    displacement: float
    cylinders: int
    configuration: str
    redline: int
    dry_weight: int
    cars: list["Car"] = Relationship(back_populates="engines", link_model=EngineCarLink)


class Transmission(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str
    cars: list["Car"] = Relationship(
        back_populates="transmissions", link_model=TransmissionCarLink
    )


class BodyStyle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    cars: list["Car"] = Relationship(
        back_populates="bodystyles", link_model=BodyStyleCarLink
    )


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)


def get_db():
    with Session(bind=engine) as session:
        yield session
