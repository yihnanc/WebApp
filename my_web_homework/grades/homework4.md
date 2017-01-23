Homework 4 Feedback
==================

Commit graded: 2e90a23020017a8083a517318baea981028a1ee9

### Incremental development using Git (10/10)

-0.1, It's good that you have a descriptive commit body, but your commit title should be descriptive too. "Thirteenth submission of homework 4" does not describe what files were changed.

### Fulfilling the grumblr specification (30/30)

### Proper Form-based validation (16/20)

-1, You should display an error message when the user enters invalid data into a form. For instance, when users log in with incorrrect password.

-3, Validation for all forms should be replaced with that of Django Forms.

### Appropriate use of web application technologies (58/60)

#### Template Inheritance and Reverse Urls (9/10)

-1, `<title>` tags for each page should contain a short textual description of what page the user is actually on. For instance, a login page could be title ‘Login’

#### Image upload (5/5)

#### Email Sending (5/5)

#### Basic ORM Usage (19/20)

-1, You do not need an additional field for first name and last name since that is already stored in the Django authentication `User` model you are using.

-0, For following, it's not necessary to make a separate model for that relation unless you want to attach additional information to that relation. Instead, a better relation to use would be the [Many-to-many relationships](https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_many/)

#### Advanced ORM Usage (10/10)

#### Routing and Requests (10/10)

### Design

### Additional Information

---
#### Total score (114/120)
---
Graded by: Kelly Cheng (kuangchc@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/yihnanc/blob/master/grades/homework4.md