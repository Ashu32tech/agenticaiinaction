import asyncio
import requests
from agents import Agent, Runner, function_tool
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

# --------------------------------
# TIME TOOL
# --------------------------------
@function_tool
def get_time(timezone: str) -> str:
    """
    Get the current time for a timezone.
    Example: New York, London, Delhi
    """
    print("Time tool executed")

    current = datetime.now().strftime("%I:%M %p")
    return f"Ashu Time is {current}"


# --------------------------------
# CALCULATOR TOOL
# --------------------------------
@function_tool
def calculate(expression: str) -> str:
    """
    Evaluate a math expression.
    Example: 25 * 4 + 10
    """
    print("Calculator tool executed")

    try:
        result = eval(expression)
        return f"Ashu {expression} = {result}"
    except Exception:
        return "Invalid expression"


# --------------------------------
# WEATHER TOOL
# --------------------------------
@function_tool
def get_weather(city: str) -> str:
    """
    Get real-time temperature for Indian cities.
    Use this tool whenever the user asks about weather or temperature.
    """
    print("Weather tool executed")

    coords = {
        "delhi": (28.61, 77.20),
        "mumbai": (19.07, 72.87),
        "bangalore": (12.97, 77.59),
        "chennai": (13.08, 80.27),
        "noida": (28.5355, 77.3910),
        "pune": (18.5204, 73.8567)
    }

    city = city.lower()

    if city not in coords:
        return "City not supported yet"

    lat, lon = coords[city]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    data = requests.get(url).json()

    temp = data["current_weather"]["temperature"]

    result = f"Ashu Current temperature in {city.title()} is {temp}°C"

    print("TOOL RESULT:", result)

    return result


# --------------------------------
# AGENT
# --------------------------------
agent = Agent(
    name="QuickAssistant",
    model="gpt-4o-mini",
    tools=[get_weather, get_time, calculate],
    instructions="""
You are a helpful assistant.

Always use tools when appropriate:

- Use calculate for math expressions
- Use get_time for time questions
- Use get_weather for weather questions

Return tool results directly without changing them.
"""
)

# --------------------------------
# MAIN
# --------------------------------
async def main():

    queries = [
        "Calculate 25 * 4 + 10",
        "What time is it in New York timezone?",
        "What's the weather like in delhi?",
    ]

    print("Processing queries in parallel...\n")

    tasks = [Runner.run(agent, q) for q in queries]

    results = await asyncio.gather(*tasks)

    for q, r in zip(queries, results):
        print("------------------------------------------------")
        print("Question:", q)
        print("Final Output:", r.final_output)
        print()

# --------------------------------
# RUN
# --------------------------------
if __name__ == "__main__":
    asyncio.run(main())