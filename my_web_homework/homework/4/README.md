1. I got point deduction last time since I submit my database to github, so this time I delete all info of my database
   Please type in the python manage.py migrate --run-syncdb before evaluate my grumblr

2. Users must confirm regitration via email, otherwise, their accounts will not be activated

3. Once users confirm their registration, they will redirect to the add profile page

4. Users are able to edit their profile if they click the their names. They will see their personal profile page.
   They can directly edit the info and click the "Edit Profile" to store what they modified(!!!!Very Important!!)

5. Users are also able to change their password via click the button in their personal profile page.
   They are not allowed to set the same password as their original one(Using form validation)
   
6. Users are not allowed to edit profile of other users. Although they will see the same design of profile page(Using template inheritance) if they click other users' name.
   They can't edit anything

7. Users are able to follow and unfollow each user by editing the "follow" and "unfollow" button at personal profile page of that user

8. Users are not able to follow themselves

9. Once users forgot their password, they can click the "Log in" button at the home page first and they will see a page which reqire them to type in their username.
   Then, they will receive an email with the link which redirect them to a page to reset their password.(Users can set the same password as previous one)
   After they successfully reset their password, they will be redirect to the log in page, so they can type in their username with new password to login

10. Users can click the "Newest Post" to view the global stream and click the  "Follower Stream" to see what their follower are doing.
    (If users don't even try to follow anyone, if they click Follower Stream, they will just stay in the same page, since their followers' table are not created)    

11. Users can post at the page "Newest Post"

12. Users only can logout if they have already logged in, vice versa

13. Non-loggin users only can review the home page

14. The "Newer" and "Older" button is still not implemented

15. Users only need to type in their first name and last name in the add profile page(don't need to type in these data at register page)

