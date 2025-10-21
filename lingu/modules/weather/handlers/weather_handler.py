from datetime import datetime, timedelta, timezone
import requests
import time

# Try to import lingu modules, fallback to defaults if not available
try:
    from lingu import cfg, log
    LINGU_AVAILABLE = True
except ImportError:
    LINGU_AVAILABLE = False
    print("Warning: 'lingu' module not found. Running in standalone mode.")
    
    # Fallback configuration function
    def cfg(module: str, key: str, default=None, env_key=None):
        # When running standalone, try environment variable first, then return default
        import os
        if env_key and env_key in os.environ:
            return os.environ[env_key]
        return default
    
    # Fallback logging function
    class log:
        @staticmethod
        def info(msg):
            print(f"INFO: {msg}")
        
        @staticmethod
        def error(msg):
            print(f"ERROR: {msg}")
            
        @staticmethod
        def err(msg):
            print(f"ERROR: {msg}")
        
        @staticmethod
        def warning(msg):
            print(f"WARNING: {msg}")
            
        @staticmethod
        def wrn(msg):
            print(f"WARNING: {msg}")
            
        @staticmethod
        def low(msg):
            print(f"DEBUG: {msg}")

api_key = cfg("weather", "api_key", env_key="OPENWEATHERMAP_API_KEY")

weather_icons = {
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "⛅",
    "broken clouds": "🌥️",
    "overcast clouds": "☁️",
    "snow": "❄️",
    "sleet": "❄️",
    "freezing": "❄️",
    "tornado": "🌪️",
    "storm": "⛈️",
    "rain": "🌧️",
    "mist": "🌫️",
    "smoke": "🌫️",
    "haze": "🌫️",
    "sand": "🌫️",
    "dust": "🌫️",
    "fog": "🌫️",
    "ash": "🌫️",
    "squalls": "🌫️"
}

wind_categories = [
    (10, 'Calm Breeze'),
    (20, 'Gentle Breeze'),
    (30, 'Light Winds'),
    (40, 'Moderate Winds'),
    (50, 'Fresh Breeze'),
    (60, 'Strong Breeze'),
    (70, 'Near Gale'),
    (80, 'Gale Winds'),
    (90, 'Severe Gale'),
    (100, 'Storm Winds'),
    (110, 'Violent Storm'),
    (120, 'Hurricane Winds'),
    (float('inf'), 'Extreme Hurricane')
]


def wind_speed_to_description(wind_speed: float) -> str:
    """
    Convert a given wind speed to its descriptive category.

    Parameters:
    - wind_speed: The speed of the wind in mph (when using imperial units)
      or km/h (when using metric units)

    Returns:
    A string description of the wind speed.
    """
    for speed, description in wind_categories:
        if wind_speed < speed:
            return description


def find_weather_icon(text):
    text_lower = text.lower()
    for keyword, icon in weather_icons.items():
        if keyword in text_lower:
            return icon
    log.wrn(f"  [weather] no icon found for {text}")
    return "?"


def get_icon_from_weather_data(datapoints):
    for item in datapoints:
        icon = find_weather_icon(item['weather'])
        if icon:
            return icon
    return "?"


def get_text_from_weather_data(datapoints):
    if len(datapoints) > 0:
        weather = datapoints[0]['weather']
        wind = datapoints[0]['wind']
        temp = datapoints[0]['temp']
        return f"{weather}, {wind}, {temp}°F"
    return "?"


def get_info_from_weather_data(datapoints):
    if len(datapoints) > 0:
        temp = datapoints[0]['temp']
        return f"{temp}"
    return "?"


def convert_to_optimized_structure(original_data):
    optimized_data = {
        "column_definitions": {
            "0": "hours_ahead",
            "1": "temperature",
            "2": "weather",
            "3": "wind"
        },
        "data": [],
        "ui_data": []
    }

    current_time_unix = time.time()
    current_time = datetime.fromtimestamp(current_time_unix, timezone.utc)

    for entry in original_data:
        entry_time_str = entry['time']

        entry_time = datetime.strptime(entry_time_str, "%d.%m.%Y %H").replace(tzinfo=timezone.utc)
        entry_time_ui = entry_time.strftime("%d.%m. %H")

        # Calculate the time difference in hours
        time_difference = entry_time - current_time
        hours_ahead = round(time_difference.total_seconds() / 3600)

        temperature = entry['temp']
        weather = entry['weather']
        wind = entry['wind']
        wind_speed = entry['wind_speed']

        optimized_data["data"].append((
            hours_ahead, temperature, weather, wind))
        optimized_data["ui_data"].append((
            f"{entry_time_ui} O'Clock",
            f"{temperature}°F",
            f"{find_weather_icon(weather)} {weather}",
            f"{wind} ({wind_speed} mph)"
        ))

    return optimized_data


def get_weather_data(city: str):
    if not api_key:
        log.err(
            "[weather] Missing OpenWeatherMap API key.\n"
            "  Open the 'settings.yaml' file and provide the API key.")
        err_str = "Can't provide weather, OpenWeatherMap API key missing"
        return [], err_str, "?", "?"

    url = (
        f"http://api.openweathermap.org/data/2.5/forecast?q={city}"
        f"&appid={api_key}&units=imperial"
    )

    log.low(f"  [weather] getting weather data for {city}")
    json_weather_data = requests.get(url).json()

    datapoints = []
    if "list" in json_weather_data:
        for item in json_weather_data["list"]:
            item_time_utc = datetime.fromtimestamp(item["dt"], timezone.utc)
            # Convert UTC to local time for display
            item_time_local = item_time_utc.astimezone()
            if item_time_utc <= datetime.now(timezone.utc) + timedelta(hours=72):
                temp = int(item['main']['temp'])
                wind_speed = int(item["wind"]["speed"])
                wind = wind_speed_to_description(wind_speed)
                weather = item["weather"][0]["description"]
                datapoints.append({
                    'time': item_time_local.strftime('%d.%m.%Y %H'),
                    'temp': temp,
                    'weather': weather,
                    'wind': wind,
                    'wind_speed': wind_speed,
                })
            else:
                break

    log.low(f"  [weather] got {len(datapoints)} datapoints")
    for datapoint in datapoints:
        log.low(f"  [weather] {datapoint['time']}: {datapoint['temp']}°F, "
                f"Weather: {datapoint['weather']}, Wind: {datapoint['wind']}")

    symbol = get_icon_from_weather_data(datapoints)
    text = get_icon_from_weather_data(datapoints)
    info = get_info_from_weather_data(datapoints)

    optimized_stucture = convert_to_optimized_structure(datapoints)
    return optimized_stucture, text, info, symbol


# Main execution loop
if __name__ == "__main__":
    print("=== Weather Handler Test ===")
    
    # Check if API key is available
    if not api_key:
        print("✗ No API key found")
        print("  Set OPENWEATHERMAP_API_KEY environment variable or configure in settings.yaml")
        exit(1)
    else:
        print("✓ API key found")
    
    # Test cities
    test_cities = ["Navasota", "Bryan", "College Station"]
    
    for city in test_cities:
        print(f"\n--- Testing weather for {city} ---")
        
        try:
            weather_data, text, info, symbol = get_weather_data(city)
            
            if weather_data:
                print(f"✓ Successfully retrieved weather for {city}")
                print(f"  Symbol: {symbol}")
                print(f"  Info: {info}")
                data_count = len(weather_data.get('data', [])) if isinstance(weather_data, dict) else 0
                print(f"  Data points: {data_count}")
                
                # Show first few data points
                if weather_data and 'ui_data' in weather_data:
                    print("  Sample forecast:")
                    for i, ui_point in enumerate(weather_data['ui_data'][:3]):
                        time_str, temp_str, weather_str, wind_str = ui_point
                        print(f"    {time_str}: {temp_str}, {weather_str}, {wind_str}")
            else:
                print(f"✗ Failed to get weather for {city}: {text}")
                
        except Exception as e:
            print(f"✗ Error getting weather for {city}: {str(e)}")
    
    print("\n=== Test Complete ===")
