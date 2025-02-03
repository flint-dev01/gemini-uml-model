sample_usecase="""
@startuml
left to right direction
skinparam usecase {{
  BackgroundColor Lavender
  BorderColor DarkSlateBlue
}}

actor "Customer" as Customer
actor "Admin" as Admin
actor "Guest" as Guest
actor "Product Manager" as ProductManager
actor "Order Manager" as OrderManager

package "E-commerce System" {{
  usecase "Register/Login" as Auth
  usecase "Browse Product Catalog" as Browse
  usecase "Search Products" as Search
  usecase "Add Product to Cart" as AddToCart
  usecase "Make Payment" as MakePayment
  usecase "Track Order" as TrackOrder
  usecase "View Order History" as ViewOrderHistory
  usecase "Manage Products" as ManageProducts
  usecase "Manage Orders" as ManageOrders
  usecase "View Sales Reports" as ViewReports
  usecase "Handle Payment Failure" as PaymentFailed
  usecase "Handle Order Delay" as OrderDelayed
}}

' Basic associations
Customer --> Auth : Register/Login
Customer --> Browse : Browse Products
Customer --> Search : Search Products
Customer --> AddToCart : Add to Cart
Customer --> MakePayment : Make Payment
Customer --> TrackOrder : Track Order
Customer --> ViewOrderHistory : View Past Orders

Admin --> ViewReports : View Performance Data
Guest --> Browse : Browse Products
Guest --> Search : Search Products

' Generalization for Admin roles
Admin <|-- ProductManager : Responsible for Products
Admin <|-- OrderManager : Responsible for Orders

' Associations for specialized Admin roles
ProductManager --> ManageProducts : Add/Update/Delete Products
OrderManager --> ManageOrders : Update Order Status
OrderManager --> HandleOrderDelayed : Handle Delayed Orders

' Relationships between use cases
AddToCart --> Browse : <<include>> Mandatory
MakePayment --> PaymentFailed : <<extend>> Payment Issues
TrackOrder --> OrderDelayed : <<extend>> Shipping Issues

' Notes
note right of Auth
  Includes:
  - Registration
  - Login
  - Password Recovery
end note

note right of Browse
  Catalog Features:
  - Categories
  - Sorting & Filtering
end note

note right of AddToCart
  Cart Operations:
  - View Cart
  - Update Quantities
  - Remove Items
end note

note right of MakePayment
  Payment Methods:
  - Credit/Debit Cards
  - PayPal, Others
  Errors trigger Payment Failure.
end note

note right of TrackOrder
  Includes updates:
  - Shipping Status
  - Delivery Notifications
  Delays trigger Order Delay handling.
end note

note right of ManageProducts
  Product Manager Tasks:
  - Add/Update/Delete
  - Set Availability & Prices
end note

note right of ManageOrders
  Order Manager Tasks:
  - View Customer Orders
  - Update Status (e.g., Delayed)
end note

note right of ViewReports
  Reports Include:
  - Sales Performance
  - Product Trends
end note
@enduml

"""