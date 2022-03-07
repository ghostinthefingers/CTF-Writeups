# FooBar CTF 2022 - Baby Rev
nothing to say just solve it ....

## solution

After the competiotion I tried to solve this challenge using angr

We are given a binary which takes a key

![Screenshot_2022-03-08_11_45_20](https://user-images.githubusercontent.com/83473054/157119242-a44535a5-3a2b-4a37-96e4-3aa505a9330e.png)

its checking lots of conditions.

this is slow and hard to solve it manually so we wrote a script using python and angr to solve it

```python
import angr
import claripy

flag_length = 42
correct_address = 0x0010287a
failure_address = [0x001028a0,0x001011F2,0x00101239,0x00101286,0x001012D4,0x00101306,0x00101354,0x00101391,0x001013CE,0x0010141C,0x00101466,0x001014A6,0x001014F4,0x00101543,0x0010157F,0x001015BB,0x001015F8,0x00101636,0x00101681,0x001016BE,0x0010170E,0x0010175D,0x0010179B,0x001017EA,0x00101800,0x00101850,0x0010188D,0x001018CB,0x00101919,0x00101956,0x00101992,0x001019CF,0x00101A09,0x00101A45,0x00101A91,0x00101ADE,0x00101B2B,0x00101B7A,0x00101BCB,0x00101C09,0x00101C57,0x00101CA8,0x00101CE4,0x00101D32,0x00101D70,0x00101DAC,0x00101DF7,0x00101E33,0x00101E6C,0x00101EAA,0x00101EE7,0x00101F24,0x00101F72,0x00101FAE,0x00101FEC,0x0010203D,0x0010208D,0x001020DD,0x0010212C,0x00102168,0x001021B6,0x00102204,0x00102242,0x00102287,0x001022D8,0x00102314,0x00102361,0x0010239E,0x001023DA,0x00102429,0x0010247A,0x001024CA,0x00102518,0x00102555,0x001025A5,0x001025F3,0x00102642,0x00102690,0x001026CE,0x0010270B,0x0010275B,0x001027A9,0x001027F8,0x00102836,0x00102873]
base_address = 0x00100000

proj = angr.Project("./chall", load_options={"auto_load_libs": False}, main_opts={"base_addr": base_address})
flag_chars = [claripy.BVS(f"flag{i}", 8) for i in range(flag_length)]
flag = claripy.Concat(*flag_chars)

state = proj.factory.full_init_state(
    args=['./chall',flag],
)

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=correct_address,avoid=failure_address)


if simgr.found:
    found = simgr.found[0]
    res = found.solver.eval(flag, cast_to=bytes)
    print(res.decode())


```

run it, it takes a while (many seconds) and then we'll get the flag

```
GLUG{C01nc1d3nc3_c4n_b3_fr3aky_T6LSERDYB6}
```
