from fastmcp import Client

async def test_server_locally(mcp):
    client = Client(mcp)
    async with client:
        ticker_result = await client.call_tool("get_ticker_chart", {"ticker": "AAPL"})
        print(ticker_result)
