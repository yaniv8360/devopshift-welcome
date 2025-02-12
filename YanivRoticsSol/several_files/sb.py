import subprocess
from sys import stdin

p = subprocess.run(["wsl", "ls", "-a", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print(p.stdout.decode())

output_bytes = p.stdout
ouptut_str = output_bytes.decode()
print(ouptut_str)
print("After")
err_bytes = p.stderr
err_str = err_bytes.decode()
print(err_str)

print(p.returncode)

# print("Before")
# p = subprocess.Popen("cmd", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
# # output = p.stdout.read(10)
# # print("After")
# output,err=p.communicate(b"exit\n")
# print(output)
# print(err)


