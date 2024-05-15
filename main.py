from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from functools import lru_cache

from models import (
    Car,
    Engine,
    Generation,
    ChassisCode,
    Make,
    Model,
    Transmission,
    Trim,
    BodyStyle,
    get_db,
    MakeResponse,
    ModelResponse,
    engine,
)
from request_models import (
    NewEngineRequest,
    NewTrimRequest,
    NewTransmissionRequest,
    NewCarRequest,
)


app = FastAPI()


@lru_cache(maxsize=1000)
def get_all_mmt_cached() -> list[MakeResponse]:
    with Session(bind=engine) as session:
        makes = session.exec(select(Make)).all()
        make_responses = []
        for make in makes:
            models = []
            for model in make.models:
                m = ModelResponse.model_validate(model)
                models.append(m)
            make_response = MakeResponse.model_validate(make)
            make_responses.append(make_response)
        return make_responses


@app.get("/all")
async def get_all(session: Session = Depends(get_db)):
    return get_all_mmt_cached()


# Makes ------


@app.get("/makes", tags=["Makes"])
async def get_makes(session: Session = Depends(get_db)) -> list[Make]:
    results = session.exec(select(Make))
    makes: list[Make] = []
    for make in results:
        makes.append(make)
    return makes


@app.post("/makes", tags=["Makes"])
async def add_make(new_make_name: str, session: Session = Depends(get_db)) -> str:
    new_make = Make(name=new_make_name)
    session.add(new_make)
    session.commit()
    session.refresh(new_make)
    return "Make added successfully."


# Models ------


@app.get("/models", tags=["Models"])
async def get_models(make_name: str, session: Session = Depends(get_db)) -> list[Model]:
    make = session.exec(select(Make).where(Make.name == make_name)).first()
    # results = session.exec(select(Model).where(Model.make == make))
    # models: list[Model] = []
    # for model in results:
    #     models.append(model)
    return make.models


@app.post("/models", tags=["Models"])
async def add_model(
    make_name: str, new_model_name: str, session: Session = Depends(get_db)
) -> str:
    models_make = session.exec(select(Make).where(Make.name == make_name)).first()

    new_model = Model(name=new_model_name, make=models_make)
    session.add(new_model)
    session.commit()
    session.refresh(new_model)
    get_all_mmt_cached.cache_clear()
    return "Model added successfully."


@app.delete("/models/{make_name}/{model_name}", tags=["Models"])
async def delete_model(
    make_name: str, model_name: str, session: Session = Depends(get_db)
) -> str:
    make = session.exec(select(Make).where(Make.name == make_name)).first()
    model = session.exec(
        select(Model).where(Model.make == make).where(Model.name == model_name)
    ).first()
    trims = session.exec(select(Trim).where(Trim.model == model)).all()
    for trim in trims:
        session.delete(trim)
        session.commit()
    session.delete(model)
    session.commit()
    return "Model deleted successfully"


# Generations ------


@app.get("/generations", tags=["Generations"])
async def get_generations(
    model_name: str, session: Session = Depends(get_db)
) -> list[Generation]:
    model = session.exec(select(Model).where(Model.name == model_name)).first()
    # results = session.exec(select(Generation).where(Generation.model == model))
    # generations: list[Generation] = []
    # for generation in results:
    #     generations.append(generation)
    return model.generations


@app.post("/generations", tags=["Generations"])
async def add_generation(
    model_name: str, generation_name: str, session: Session = Depends(get_db)
) -> str:
    generations_model = session.exec(
        select(Model).where(Model.name == model_name)
    ).first()

    new_generation = Generation(name=generation_name, model=generations_model)
    session.add(new_generation)
    session.commit()
    session.refresh(new_generation)
    return "Generation added successfully."


# ChassisCodes ------


@app.get("/chassiscodes", tags=["Chassis Codes"])
async def get_chassis_codes(
    generation_name: str, session: Session = Depends(get_db)
) -> list[ChassisCode]:
    generation = session.exec(
        select(Generation).where(Generation.name == generation_name)
    ).first()
    # results = session.exec(select(Generation).where(Generation.model == model))
    # generations: list[Generation] = []
    # for generation in results:
    #     generations.append(generation)
    return generation.chassis_codes


@app.post("/chassiscodes", tags=["Chassis Codes"])
async def add_chassis_code(
    model_name: str,
    generation_name: str,
    chassis_code_name: str,
    session: Session = Depends(get_db),
) -> str:
    generations_model = session.exec(
        select(Model).where(Model.name == model_name)
    ).first()

    chassis_code_generation = session.exec(
        select(Generation)
        .where(Generation.model == generations_model)
        .where(Generation.name == generation_name)
    ).first()

    new_chassis_code = ChassisCode(
        name=chassis_code_name, generation=chassis_code_generation
    )
    session.add(new_chassis_code)
    session.commit()
    session.refresh(new_chassis_code)
    return "Chassis Code added successfully."


# Trims ------


@app.get("/trims", tags=["Trims"])
async def get_trims(model_name: str, session: Session = Depends(get_db)) -> list[Trim]:
    model = session.exec(select(Model).where(Model.name == model_name)).first()
    # results = session.exec(select(Trim).where(Trim.generation == generation))
    # trims: list[Trim] = []
    # for trim in results:
    #     trims.append(trim)
    return model.trims


@app.post("/trims", tags=["Trims"])
async def add_trim(trim: NewTrimRequest, session: Session = Depends(get_db)) -> str:
    trims_model = session.exec(select(Model).where(Model.name == trim.model)).first()

    new_trim = Trim(name=trim.name, model=trims_model)
    session.add(new_trim)
    session.commit()
    session.refresh(new_trim)
    return "Trim added successfully."


# Engines ------


@app.get("/engines", tags=["Engines"])
async def get_engines(session: Session = Depends(get_db)) -> list[Engine]:
    results = session.exec(select(Engine))
    engines: list[Engine] = []
    for engine in results:
        engines.append(engine)
    return engines


@app.post("/engines", tags=["Engines"])
async def add_engine(
    new_engine: NewEngineRequest, session: Session = Depends(get_db)
) -> str:
    engine = Engine.model_validate(new_engine)
    session.add(engine)
    session.commit()
    session.refresh(engine)
    return "Engine added successfully."


# Transmissions ------


@app.get("/transmissions", tags=["Transmissions"])
async def get_transmissions(session: Session = Depends(get_db)) -> list[Transmission]:
    results = session.exec(select(Transmission))
    transmissions: list[Transmission] = []
    for transmission in results:
        transmissions.append(transmission)
    return transmissions


@app.post("/transmissions", tags=["Transmissions"])
async def add_transmission(
    new_transmission: NewTransmissionRequest, session: Session = Depends(get_db)
) -> str:
    transmission = Transmission.model_validate(new_transmission)
    session.add(transmission)
    session.commit()
    session.refresh(transmission)
    return "Transmission added successfully."


@app.put("/transmissions/{transmission_name}", tags=["Transmissions"])
async def update_transmissions(
    transmission_name: str,
    updated_transmission: NewTransmissionRequest,
    session: Session = Depends(get_db),
):
    transmission = session.exec(
        select(Transmission).where(Transmission.name == transmission_name)
    ).one()
    transmission.name = updated_transmission.name
    transmission.type = updated_transmission.type
    session.add(transmission)
    session.commit()
    session.refresh(transmission)


@app.delete("/transmissions/{transmission_name}", tags=["Transmissions"])
async def delete_transmissions(
    transmission_name: str, session: Session = Depends(get_db)
):
    transmission = session.exec(
        select(Transmission).where(Transmission.name == transmission_name)
    ).first()
    session.delete(transmission)
    session.commit()


# Cars ------


@app.get("/cars", tags=["Cars"])
async def get_cars(trim_name: str, session: Session = Depends(get_db)) -> list[Car]:
    trim = session.exec(select(Trim).where(Trim.name == trim_name)).first()
    # results = session.exec(select(Trim).where(Trim.generation == generation))
    # trims: list[Trim] = []
    # for trim in results:
    #     trims.append(trim)
    return trim.cars


@app.post("/cars", tags=["Cars"])
async def add_car(
    trim_name: str,
    chassis_code_name: str,
    car_request: NewCarRequest,
    session: Session = Depends(get_db),
) -> str:
    trim = session.exec(select(Trim).where(Trim.name == trim_name)).first()
    chassis_code = session.exec(
        select(ChassisCode).where(ChassisCode.name == chassis_code_name)
    ).first()

    new_car = Car(
        year=car_request.year,
        trim=trim,
        chassis_code=chassis_code,
        weight=car_request.weight,
        length=car_request.length,
        width=car_request.width,
    )

    for eng in car_request.engines:
        e = session.exec(select(Engine).where(Engine.name == eng.name)).first()
        if e is None:
            e = Engine.model_validate(eng)
        new_car.engines.append(e)

    for transmission in car_request.transmissions:
        trans = session.exec(
            select(Transmission).where(Transmission.name == transmission.name)
        ).first()
        if trans is None:
            trans = Transmission.model_validate(transmission)
        new_car.transmissions.append(trans)

    for bodystyle in car_request.bodystyles:
        bs = session.exec(
            select(BodyStyle).where(BodyStyle.name == bodystyle.name)
        ).first()
        if bs is None:
            bs = BodyStyle.model_validate(bodystyle)
        new_car.bodystyles.append(bs)

    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return "Car added successfully."
