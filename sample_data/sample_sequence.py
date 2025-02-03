sample_sequence="""
@startuml
autonumber

actor User as U
participant "Frontend" as FE
participant "Backend" as BE
database "Order Database" as DB
participant "Authentication Service" as AS

' 1. User accesses the login page
U -> FE: Open website
FE -> U: Display login page

' 2. User submits credentials
U -> FE: Submit username and password
FE -> BE: Send credentials for authentication

' 3. Backend checks user in database
BE -> DB: Query user by username
DB --> BE: Return user data

alt User found
    ' 4. Backend compares password
    BE -> BE: Validate password

    alt Password matches
        ' 5. Generate authentication token
        BE -> AS: Generate JWT token
        AS --> BE: Return JWT token

        ' 6. Send success response
        BE -> FE: Send success response
        FE -> U: Redirect to dashboard
    else Password incorrect
        ' 7. Handle incorrect password
        BE -> FE: Send failure response
        FE -> U: Display error response
    end
else User not found
    ' 8. Handle non-existent user
    BE -> FE: Send failure response
    FE -> U: Display error response
end

@enduml

"""