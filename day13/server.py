import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")


@mcp.tool()
def get_current_temperature(latitude: float, longitude: float) -> str:
    """Get the current temperature and wind speed for a place, given its latitude and longitude."""
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": latitude, "longitude": longitude, "current_weather": True},
        timeout=10,
    )
    response.raise_for_status()
    weather = response.json()["current_weather"]
    return f"{weather['temperature']} C, wind {weather['windspeed']} km/h"


@mcp.tool()
def celsius_to_fahrenheit(celsius: float) -> str:
    """Convert a temperature from Celsius to Fahrenheit."""
    return f"{celsius * 9 / 5 + 32:.1f} F"


if __name__ == "__main__":
    mcp.run()