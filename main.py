import uuid
import asyncio
import argparse
from fastmcp import FastMCP, Image
from PIL import Image as PILImage
from io import BytesIO

from src.stock import load_dataframe
from src.ssm import caluculate_trend_level
from src.alt import create_trend_season_chart, create_actual_level_chart, concat_chart_vertically
from src.dev import test_server_locally

# MCP
mcp = FastMCP("create-timeseries-chart")

@mcp.tool()
def get_ticker_chart(ticker: str) -> Image:
    """Get a chart for a given ticker"""
    df = load_dataframe(ticker, period="2y")
    forecast_df = caluculate_trend_level(df)
    forecast_df = forecast_df[forecast_df['date'] >= "2024-06-01"]

    buffer = BytesIO()
    filename = f'tmp/{uuid.uuid4()}.png'
    upper_chart = create_actual_level_chart(forecast_df)
    lower_chart = create_trend_season_chart(forecast_df)
    final_chart = concat_chart_vertically(upper_chart, lower_chart)
    final_chart.save(filename)
    PILImage.open(filename).save(buffer, format="PNG")
    return Image(data=buffer.getvalue(), format="png")


# Run the server if '--prod' is passed as an argument
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a time series chart for a stock ticker.")
    parser.add_argument("--prod", type=str, nargs="?", default="false", help="Run in production mode (true/false)")
    args = parser.parse_args()

    if args.prod == "true":
        mcp.run()
    else:
        asyncio.run(test_server_locally(mcp))
