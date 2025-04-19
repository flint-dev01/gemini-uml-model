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
    chat1, chat2 ,chat3 = InitializeModel()
    plantuml_web_server =  InitializePlantUmlServer()
    human = usecase_human(text.srs_text)
    usecase_prompt = ChatPromptTemplate.from_messages([("system", usecase_system), ("human", human)])
    usecase_chain = usecase_prompt | chat1    
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


async def process_seuence(use_case, chat, plantuml_web_server, data):
    try:
        # Generate prompt
        system_msg = sequence_system(use_case)
        human_msg = sequence_human(use_case, data.srs_text, data.usecase_code)
        sequence_prompt = ChatPromptTemplate.from_messages([("system", system_msg), ("human", human_msg)])

        # Invoke chat asynchronously
        sequence_chain = sequence_prompt | chat
        sequence_result = await sequence_chain.ainvoke({})  # Ensure awaiting the coroutine
        
        seq_code = extract_plantuml_code(sequence_result.content)

        # Validate and process UML code
        if not seq_code or not seq_code.strip().startswith("@startuml") or not seq_code.strip().endswith("@enduml"):
            print(f"Invalid PlantUML code for {use_case}. Skipping...")
            return None
        
        label = re.sub(r"[^\w\-_.]", "_", use_case.replace(" ", "_"))
        print(f"Processing diagram: {label}")

        # Generate image
        image_bytes = plantuml_web_server.processes(seq_code)
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        # Store results
        return {"label": label, "image": encoded_image}

    except Exception as e:
        print(f"Error processing {use_case}: {e}")
        return None

async def process_activity(actor, chat, plantuml_web_server, data):
    try:
        system_msg = activity_system(actor)
        human_msg = activity_human(actor, data.srs_text, data.usecase_code)
        activity_prompt = ChatPromptTemplate.from_messages([("system", system_msg), ("human", human_msg)])

        # Invoke chat1
        activity_chain = activity_prompt | chat
        activity_result = await activity_chain.ainvoke({})
        act_code = extract_plantuml_code(activity_result.content)
        # Validate and process UML code
        if not act_code.strip().startswith("@startuml") or not act_code.strip().endswith("@enduml"):
            print(f"Invalid PlantUML code for {actor}. Skipping...")
            return None

        # Generate image
        image_bytes = plantuml_web_server.processes(act_code)
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        # Store results
        return ({"label": actor, "image": encoded_image})

    except Exception as e:
        print(f"Error processing {actor}: {e}")
        return None

async def CreateSequence(data):
    chat1, chat2 , chat3 = InitializeModel()
    plantuml_web_server = InitializePlantUmlServer()

    tasks = []
    for idx, use_case in enumerate(data.use_cases):
        chat = chat3 if idx % 2 == 0 else chat2 
        tasks.append(process_seuence(use_case, chat, plantuml_web_server, data))

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Filter out None values (failed cases)
    sequence_image_data = [result for result in results if result is not None]

    return sequence_image_data


async def CreateActivity(data: ActivityCreate):
    chat1, chat2, chat3 = InitializeModel()
    plantuml_web_server = InitializePlantUmlServer()
    activity_image_data = [] 
    tasks = []
    for idx, actor in enumerate(data.actors):
        chat = chat1 if idx % 2 == 0 else chat2 
        tasks.append(process_activity(actor, chat, plantuml_web_server, data))
    results = await asyncio.gather(*tasks)

    activity_image_data = [result for result in results if result is not None]

    return activity_image_data
