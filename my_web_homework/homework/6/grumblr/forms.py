from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from models import *

class ResetPwdForm(forms.Form):
    username = forms.CharField(max_length = 20,
    widget=forms.TextInput(attrs={'placeholder': 'Username',"class":"TextType"})
    )

    # Customizes form validation for the email field.
    def clean(self):
        cleaned_data = super(ResetPwdForm, self).clean()
        # Confirms that the username is not already present in the
        # User model database.
        username = cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("User does not exist")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return cleaned_data

class RealResetPwdForm(forms.Form):
    new_passwd1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "New Password","class":"TextType"})
    )
    new_passwd2 = forms.CharField(max_length = 200, 
                                label='Confirm New Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "Confirm New Passwd","class":"TextType"})
    )
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RealResetPwdForm, self).clean()

        # Confirms that the two password fields match
        new_passwd1 = cleaned_data.get('new_passwd1')
        new_passwd2 = cleaned_data.get('new_passwd2')
        if new_passwd1 and new_passwd2 and new_passwd1 != new_passwd2:
            raise forms.ValidationError("Passwords did not match.")


        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class ChangePwdForm(forms.Form):
    old_passwd = forms.CharField(max_length = 200, 
                                label='Old Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "Old Password","class":"TextType"})
    )
    new_passwd1 = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "New Password","class":"TextType"})
    )
    new_passwd2 = forms.CharField(max_length = 200, 
                                label='Confirm New Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "Confirm New Passwd","class":"TextType"})
    )
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePwdForm, self).clean()

        # Confirms that the two password fields match
        new_passwd1 = cleaned_data.get('new_passwd1')
        new_passwd2 = cleaned_data.get('new_passwd2')
        old_passwd = cleaned_data.get('old_passwd')
        if new_passwd1 and new_passwd2 and new_passwd1 != new_passwd2:
            raise forms.ValidationError("Passwords did not match.")

        if new_passwd1 and old_passwd and new_passwd1 == old_passwd:
            raise forms.ValidationError("New password should not be the same as the old one.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20,
    widget=forms.TextInput(attrs={'placeholder': 'Username',"class":"TextType"})
    )
    password = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "Password","class":"TextType"})
    )
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(LoginForm, self).clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username doesn't exist.")
        
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Password.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data



class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20,
    widget=forms.TextInput(attrs={'placeholder': 'Username',"class":"TextType"})
    )
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={"placeholder": "Password","class":"TextType"})
    )
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={"placeholder": "Confirm Password","class":"TextType"})
    )
    
    email = forms.EmailField(max_length = 30,
    widget=forms.TextInput(attrs={'placeholder': 'Email','class':'TextType'})
    )
    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    # Customizes form validation for the email field.
    def clean_email(self):
        # Confirms that the username is not already present in the
        # User model database.
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return email
       
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('owner', )
        widgets = {'picture' : forms.FileInput()}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        #only verify post content
        exclude = ('users', 'time', 'created_date')
    def clean_post(self):
        post = self.cleaned_data.get('post')
        if not post or len(post) > 50:
            raise forms.ValidationError("Please input text length between 1 and 50")
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #only verify post content
        exclude = ('users', 'postid', 'created_date', 'time')
    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if not comment or len(comment) > 50:
            raise forms.ValidationError("Please input the text length between 1 and 50")
        print("sgfhdh")
        print(comment)
        return comment
