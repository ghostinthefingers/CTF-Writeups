# defcon30 speedrun - syscall-me-maybe

after a quick look you see the challenge get a value and save in rdi, then rsi, rdx, r10, r8 and r9, then ask you about your syscall number.

![Screenshot_2022-09-02_23_46_22](https://user-images.githubusercontent.com/83473054/188107346-0f0837e8-e640-4325-bd4b-db9ebcf4894a.png)

I did checksec on this bin file
pie is enabled.

## exploit
