import sys
from calculator.engine import evaluate, CalcError

BANNER = "Simple Calculator (type :q to quit)"

def repl():
    print(BANNER)
    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if line in {":q", ":quit", "exit"}:
            break
        if not line:
            continue

        try:
            result = evaluate(line)
            print(result)
        except ZeroDivisionError:
            print("Error: division by zero")
        except CalcError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            print(evaluate(expr))
        except Exception as e:
            print(f"Error: {e}")
    else:
        repl()
