import subprocess

def say_hello(name):
    return f"Hello, {name}!"

# ❌ Insecure call (Bandit & Semgrep will catch this)
def insecure_code():
    user_input = "ls"  # Imagine this is untrusted input
    subprocess.call(user_input, shell=True)

if __name__ == "__main__":
    print(say_hello("World"))
    insecure_code()

