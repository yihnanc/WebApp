Project Specification Feedback
==================

Commit graded: 

### The product backlog (10/10)

Your backlog is pretty detailed, but can be improved:
* A spreadsheet-like format is easier to read for backlogs, rather than bulleted lists. You can also explore existing online tools for generating and tracking work on a project. 
* You should have a clear assignment of responsibility for each feature, to the team member(s) who will complete that feature. Each student should have sole responsibility for some features on the overall project. An easy way to organize this is to have a column in your spreadsheet recording the responsible team member.
* You should do a cost estimate for each feature, in hours. If the cost estimate is more than 5 or 8 hours, consider breaking the feature into smaller work units to improve your ability to track progress on it.

### Data models (9/10)

* You should probably also store longitude and latitude for your location in the `Event` model.
* You should have a OneToOne relationship in the `Profile` model to Django's `User`.
* Missing friend field for `Profile`
* Missing participant field in `Event`.
* Consider having start and end time in `Event`.
* Will you have a notification model? How will you keep track of the RSVPs to an invitation?

### Wireframes or mock-ups (10/10)

Pretty detailed! So if I want to see a list of people I follow, would I have to do this in the search box? 

### Additional Information

It's cool that you have shortcuts for searching, but it would probably be a better user experience if there were clear filters somewhere. If you don't want it to take up space, you could have the filters expand out when clicked.

---
#### Total score (29/30)
---
Graded by: Kelly Cheng (kuangchc@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team216/blob/master/feedback/specification-feedback.md