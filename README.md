## [Welcome to Not Reddit](https://not-reddit-4131.herokuapp.com/)
### How to use the application    
There are four views (main feed, comment section, post section, profile section).   
   
The first view when you land on our website, is a view of the current posts from all the users; main feed.   

At this view, you have options to ```sign up``` with our website or ```login``` if you've already registered. 
You are restricted from commenting, viewing comments, seeing user's profiles or upvoting, but you may visit the links in the posts by clicking the thumbnail or title.     

#### TL;DR - Should work like any social media website (but more like old.reddit.com)
###### Logged out    
1. Click the ```Sign Up``` button to register, or ```Login``` if you've already registered.    

2. You will be redirected to ```\register``` where you need to provide a username and matching passwords.    

3. If all is good, you will be redirected to ```\login``` where you can use your registration username and password to login    

###### Logged In    
4. If successful, you get redirected back to the main feed page. ```\```     

5. You now have options to ```Logout```, ```Post Item``` or go to ```{your_username}``` at the navbar.    

6. On the main page you will see the same posts you saw before you logged in, but now you could upvote/downvote on a post, go to ```comments``` and view other user's comments or post your own comments, or view other user's profiles. If you comment, your comment goes to the bottom of the list (just like reddit).      

7. If you click ```Logout``` you get sent to ```\logout``` which ends your session but redirects to the main feed again (with you logged out), then then you can restart this list but choose ```Login``` to skip registration.     

8. If you click ```Post Item``` you get redirected to ```\post``` where you may post a link and a title.         

9. Once you do step 8 ^, you will get redirected to ```comments\id:post_id``` where post_id is the number of your post in our database.    

10. Your post will be thumbnailed and posted to the top of the comment section, you may comment on it, your post will also be posted to the top of the main feed.    

11. Click ```{your_username}``` you will get redirected to ```\profile\id:user_id``` where user_id is your number based on how many users are in the database.     

12. You may see your posts here, if you've posted any. You also see how many votes you have.    

13. Posts on profile are displayed in a similar manner to posts on the main feed, so you may apply the same actions (vote, comments, go to actual link, or click on your own username[refreshes page])     

14. You may click on the Red logo on top left on any view including login and signup views, to go back to the main feed.        
