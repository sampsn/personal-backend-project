import json
import os
from sqlmodel import Session, select
from models import Make, Model, Trim, engine


# if os.path.exists(os.path.join(os.path.dirname(__file__), "database.db")) is False:
folder_path = "carjsons"
jsonfiles = [
    file
    for file in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, file))
]

for file in jsonfiles:
    with open("carjsons/" + file, "r") as f:
        data = json.load(f)
        make_name = file[:-5]
        add_make = Make(name=make_name)
        with Session(bind=engine) as session:
            session.add(add_make)
            session.commit()
            session.refresh(add_make)

        # print("-------------" + make_name + "--------------")
        for model in data:
            # print("----" + model["model"] + "-----")
            add_model = Model(name=model["model"], make=add_make)
            with Session(bind=engine) as session:
                session.add(add_model)
                session.commit()
                session.refresh(add_model)
            for trim in model["trims"]:
                # print(trim["name"])
                add_trim = Trim(name=trim["name"], model=add_model)
                with Session(bind=engine) as session:
                    session.add(add_trim)
                    session.commit()
                    session.refresh(add_trim)

with Session(bind=engine) as session:
    makes = session.exec(select(Make))

    for make in makes:
        print(make.name)
        for model in make.models:
            print(model.name)
            for trim in model.trims:
                print(trim.name)
