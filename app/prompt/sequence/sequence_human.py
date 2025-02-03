def sequence_human(use_case,srs_text,usecase_code):
    sequence_human = f"""
        Generate **PlantUML {use_case} feature sequence diagram** based on the provided Software Requirements Specification (SRS). 
        It should be a detailed sequence diagram adhering to these guidelines:

        ### Guidelines:

        1. **Actors**:
        - Represent users or external systems as actor in PlantUML.

        2. **Participants**:
        - Represent system components or services as participant.

        3. **Messages**:
        - Use -> for synchronous communication and --> for asynchronous messages.
        - Include responses and feedback loops.

        4. **Activations**:
        - Highlight active periods using activate and deactivate.

        5. **Conditional Logic**:
        - Use alt for branching paths and opt for optional steps.

        ### SRS Input:
        {srs_text}

        ### Useacse of SRS :
        {usecase_code}

        NOTE:
        Include **only** PLantuml Code. no other text
        Through this SRS and UseCase only make sequnce diagram for this "{use_case}" feature.
        The diagram should specifically be only for that feature not for any other feature.
        """
    return sequence_human