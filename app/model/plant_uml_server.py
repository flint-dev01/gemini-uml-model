from plantuml import PlantUML

def InitializePlantUmlServer():
    plantuml_url = "http://www.plantuml.com/plantuml/img/"
    plantuml = PlantUML(url=plantuml_url)
    return plantuml
