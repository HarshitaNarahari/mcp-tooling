import asyncio
from agent3_server import calculate, evaluate_expression

async def main():
    print("Testing math evaluation...")
    tests = [
        "2 + 3 * 4",
        "(10 - 3) ** 2",
        "50 / 5 + 6",
        "3 * (2 + 4) - 5",
        "-7 + 2"
    ]

    for expr in tests:
        result = calculate(expr)
        print(f"Expression: {expr}")
        print(f"Output: {result}")
        print("-" * 30)

    print("Testing evaluate_expression directly...")
    print(evaluate_expression("8 / 2 * (3 + 1)"))

if __name__ == "__main__":
    asyncio.run(main())
