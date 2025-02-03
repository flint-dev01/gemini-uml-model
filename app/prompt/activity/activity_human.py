def activity_human(actor,srs_text,usecase_code):
    activity_human = f"""
    Generate a **PlantUML activity diagram** for the **{actor}** role, based on the provided Software Requirements Specification (SRS).
    The diagram should adhere to the following guidelines:

    ### Guidelines:

    1. **Activities**:
       - Represent steps as activity nodes.

    2. **Conditional Flow**:
       - Use `if` and `else` to show conditions between steps.

    3. **Decisions**:
       - Use diamond nodes to indicate branching logic.

    4. **Start and End**:
       - Clearly show process start and end points.

    5. **Swimlanes**:
       - Organize tasks in swimlanes between the **{actor}** and relevant system components.

    ### SRS Input:
    {srs_text}

    ### Use Case of SRS:
    {usecase_code}

    NOTE:
    Include **only** PlantUML code for the **{actor}**. Do not include any other text.
    """
    return activity_human