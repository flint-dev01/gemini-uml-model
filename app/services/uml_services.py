import asyncio
import aiofiles
import base64
import re
import uuid
import os
from fastapi import Response
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.uml_schema import UsecaseCreate, SequenceCreate ,ActivityCreate
from app.model.llama3_1_8b_instant import InitializeModel
from app.model.plant_uml_server import InitializePlantUmlServer
from app.prompt.usecase.usecase_system import usecase_system
from app.prompt.usecase.usecase_human import usecase_human
from app.prompt.sequence.sequence_human import sequence_human
from app.prompt.sequence.sequence_system import sequence_system
from app.prompt.activity.activity_system import activity_system
from app.prompt.activity.activity_human import activity_human

async def save_image_and_return(image_bytes: bytes) -> str:
    unique_filename = f"usecase_{uuid.uuid4().hex}.png"
    save_path = os.path.join("use_case_folder", unique_filename)
    os.makedirs("use_case_folder", exist_ok=True)

    async with aiofiles.open(save_path, "wb") as img_file:
        await img_file.write(image_bytes)
        print("saved")

    return save_path

async def delete_image(file_path: str):
    if os.path.exists(file_path):
        print("found", file_path)
        os.remove(file_path)

def extract_plantuml_code(text: str):
    """Extracts the PlantUML code from the generated text."""
    pattern = r"@startuml.*?@enduml"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0) if match else None

async def CreateUseCase(text: UsecaseCreate):
    model = InitializeModel()
    plantuml_web_server =  InitializePlantUmlServer()
    human = usecase_human(text.srs_text)
    usecase_prompt = ChatPromptTemplate.from_messages([("system", usecase_system), ("human", human)])
    usecase_chain = usecase_prompt | model    
    usecase_result = await asyncio.to_thread(usecase_chain.invoke, {}) 
    structured_text = extract_plantuml_code(usecase_result.content)
    if not structured_text:
        return Response(content="Failed to extract PlantUML code", media_type="text/plain")
    try:
        image_bytes = await asyncio.to_thread(plantuml_web_server.processes, structured_text)
    except Exception:
        return Response(content="Failed to extract PlantUML code", media_type="text/plain")
    
    usecase_code = structured_text.replace("{\n", "{{\n").replace("\n}", "\n}}")
    use_cases = re.findall(r'usecase "([^"]+)"', structured_text)
    if "Login/Signup" in use_cases:
        use_cases.remove("Login/Signup")
        use_cases.append("Login")
        use_cases.append("Signup")
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    actors = re.findall(r'actor\s+"([^"]+)"', structured_text)
    # usecase_saved_image_path = await save_image_and_return(image_bytes)
    # usecase_file = FileResponse(
    #     usecase_saved_image_path, 
    #     media_type="application/octet-stream", 
    #     headers={"Content-Disposition": f"attachment; filename={os.path.basename(usecase_saved_image_path)}"}
    # )

    # background_tasks.add_task(delete_image, usecase_saved_image_path)
    response_data = {
            "use_case_diagram": encoded_image,
            "usecase_code":usecase_code,
            "use_cases":use_cases,
            "actors":actors
        }
    return response_data


async def CreateSequence(data: SequenceCreate):
    model = InitializeModel()
    plantuml_web_server = InitializePlantUmlServer()
    sequence_image_data = []

    for use_case in data.use_cases:
        try:
            # Generate prompt
            system_msg = sequence_system(use_case)
            human_msg = sequence_human(use_case, data.srs_text, data.usecase_code)
            sequence_prompt = ChatPromptTemplate.from_messages([("system", system_msg), ("human", human_msg)])

            # Invoke model
            sequence_chain = sequence_prompt | model
            sequence_result = sequence_chain.invoke({})
            seq_code = extract_plantuml_code(sequence_result.content)

            # Validate and process UML code
            if not seq_code or not seq_code.strip().startswith("@startuml") or not seq_code.strip().endswith("@enduml"):
                print(f"Invalid PlantUML code for {use_case}. Skipping...")
                continue
            
            label = re.sub(r"[^\w\-_.]", "_", use_case.replace(" ", "_"))
            print(f"Processing diagram: {label}")
            # Generate image
            image_bytes = plantuml_web_server.processes(seq_code)
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            # Store results
            sequence_image_data.append({"label": label, "image": encoded_image})

        except Exception as e:
            print(f"Error processing {use_case}: {e}")

    return sequence_image_data


async def CreateActivity(data: ActivityCreate):
    model = InitializeModel()
    plantuml_web_server = InitializePlantUmlServer()
    activity_image_data = [] 
    for actor in data.actors:
        try:
            # Generate prompt
            system_msg = activity_system(actor)
            human_msg = activity_human(actor, data.srs_text, data.usecase_code)
            activity_prompt = ChatPromptTemplate.from_messages([("system", system_msg), ("human", human_msg)])

            # Invoke model
            activity_chain = activity_prompt | model
            activity_result = activity_chain.invoke({})
            act_code = extract_plantuml_code(activity_result.content)
            # Validate and process UML code
            if not act_code.strip().startswith("@startuml") or not act_code.strip().endswith("@enduml"):
                print(f"Invalid PlantUML code for {actor}. Skipping...")
                continue
            
           

            # Generate image
            image_bytes = plantuml_web_server.processes(act_code)
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            # Store results
            activity_image_data.append({"label": actor, "image": encoded_image})

        except Exception as e:
            print(f"Error processing {actor}: {e}")

    return activity_image_data
