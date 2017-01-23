1. I used Amazon Elastic Beanstalk as my platform for deployment

2. I set all the secret keys in the configuration of Amazon EB and
   use os.environ to access the confidential data in the Amazon EB

3. I used hotmail smtp server to help me send the confirmation mail since
   I didn't successfully set gmail smtp server due to the security issue

4. I used postgres as my database

5. The following is my reference:
   https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

   https://realpython.com/blog/python/deploying-a-django-app-and-postgresql-to-aws-elastic-beanstalk/  

6. Here is my URL for deployed application:
   http://yorkchiu0528.us-east-1.elasticbeanstalk.com
