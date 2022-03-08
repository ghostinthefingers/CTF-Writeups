import angr
import claripy
import sys



proj = angr.Project("./matrix")
# flag_chars = [ claripy.BVS(f"flag_chars{i}",8) for i in range(flag_length)]
# flag = claripy.Concat(*flag_chars + [claripy.BVV('\n', 8)])

state = proj.factory.entry_state()

# for k in flag_chars:
#     state.solver.add(k >= ord('!'))
#     state.solver.add(k <= ord('~'))

simgr = proj.factory.simgr()
simgr.run()


if simgr.deadended:
    for s in simgr.deadended:
        tmp = s.posix.dumps(0)
        if b"glug" in tmp.lower():
            print(tmp)






