# syscallDB
## x86 and x64 syscall database
Have you ever been doing some assembly and finding yourself looking furiously for some nisch syscall\
Well, that will no longer be a problem with syscallDB's reverse lookup, did you forget rax for execve?
## x86
```py
import sysDB
sysDB.syscall32(0) # gives syscall 0
sysDB.syscall32("exec") # gives all syscalls with "exec" in their name
```
## x64
```py
import sysDB
sysDB.syscall64(0) # gives syscall 0
sysDB.syscall64("exec") # gives all syscalls with "exec" in their name
```

