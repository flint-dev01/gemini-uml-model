sample_activity="""
@startuml
!define RECTANGLE_STYLE <<rectangle>>
!define PARTITION_STYLE <<partition>>

' Styling to make the diagram more professional
<style>
activityDiagram {{
  BackgroundColor #F5F5F5
  BorderColor #333
  FontColor #333
  FontName Arial
}}

partition {{
  LineColor #4CAF50
  FontColor black
  BackgroundColor Lavender
}}

note {{
  FontColor #FFFFFF
  BackgroundColor #3E8E41
}}
</style>

start

' Partition for user actions
partition "User Login" {{
  :Enter username and password;
  :Submit login details;
  if (Login successful?) then (yes)
    :Redirect to homepage;
  else (no)
    :Show error message;
    stop
  endif
}}

' Partition for browsing products
partition "Product Browsing" {{
  :View product categories;
  :Filter products based on price, ratings, etc.;
  :View product details;
  :Add product to wishlist or cart;
}}

' Partition for shopping cart management
partition "Shopping Cart" {{
  :View cart items;
  :Modify quantity or remove item;
  :Proceed to checkout;
}}

' Partition for checkout process
partition "Checkout" {{
  :Enter shipping address;
  :Choose payment method;
  :Enter payment details;
  if (Payment successful?) then (yes)
    :Confirm order;
    :Send confirmation email;
    :Redirect to order summary page;
  else (no)
    :Show payment error message;
    stop
  endif
}}

' Partition for order summary
partition "Order Summary" {{
  :Display order details;
  :Provide order tracking option;
  :Thank customer for the purchase;
}}

stop

@enduml
"""