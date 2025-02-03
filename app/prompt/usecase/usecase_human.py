
def usecase_human(srs_text):
    usecase_human = f"""
        A **use case diagram** models the interaction between actors and a system, focusing on the system's functionalities. Here are its key features:

        ### 1. **Actors**
        - Represent users, other systems, or hardware interacting with the system.
        - Depicted as stick figures in the diagram.

        ### 2. **Use Cases**
        - Represent services or functionalities the system provides.
        - Depicted as ovals, such as *Login*, *Place Order*, *Generate Report*.

        ### 3. **Relationships**
        - **Association**: Links actors to use cases.
        - **Include**: Indicates mandatory inclusion of another use case.
        - **Extend**: Represents optional or conditional behavior.
        - **Generalization**: Highlights inheritance between actors or use cases.

        ### 4. **System Boundary**
        - Encapsulates the system's scope.
        - Depicted as a rectangle containing the use cases.

        ### 5. **Simplification and Focus**
        - Focuses on "what" the system does, not "how" it works.
        - Suitable for high-level discussions.

        ### Software Requirements Specification (SRS):
        {srs_text}

        Based on the SRS provided, generate the corresponding PlantUML code for a use case diagram.
        """
    return usecase_human