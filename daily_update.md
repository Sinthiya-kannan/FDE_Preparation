# FDE Preparation – Daily Study Update

## Day 1 – Yesterday

### Topics Studied

* Understood the role and responsibilities of a Forward Deployed Engineer (FDE).
* Learned about custom solution development and client-specific integrations.
* Understood the FDE workflow from requirement gathering to deployment and production support.
* Practiced requirement analysis for a Customer Registration module.
* Defined business rules and validations.
* Designed Customer and User database tables.
* Designed an Invitation table with:

  * Invitation ID
  * User ID
  * UUID token
  * Sent date/time
  * 7-day expiry
  * Invitation status
* Discussed customer approval/rejection and user invitation flow.
* Learned how to prevent duplicate customer registration using the company domain and a unique database constraint.

## Day 2 – Today

### Topics to Study

* Python for backend development
* FastAPI fundamentals
* REST API concepts
* GET, POST, PUT, PATCH and DELETE
* Request and response handling
* Pydantic models and validation
* HTTP status codes
* Exception handling
* API testing using Postman

### Practical Task

I will start implementing the **Customer Registration API** using Python and FastAPI based on the requirements and database design created yesterday.

### API

`POST /customers/register`

### Goal

Understand and implement the flow:

Client Requirement → API Design → FastAPI → Validation → Business Logic → Response
