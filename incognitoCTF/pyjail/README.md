#incognito CTF 2022

##pyjail 1

a python jail challenge which was filtering ```__``` so we couldn't call ```__builtins__``` or etc.
after some fuzzing I found that ```%``` is also filtered. so there was an idea for me


in fuzzing part I got that ```__``` will be replaced with nothing, ```%``` also replaced with nothing.

THE IDEA =>  what if we write ```_%_```. yes, ```%``` would be replaced with nothing and now we have ```__``` :)

so let's write our payload.



