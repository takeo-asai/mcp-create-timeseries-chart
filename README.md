# MCP create timeseries chart

> [!NOTE]
> `2025/05/04` 時点では VSCode の GitHub Copilot Chat の Agent Mode で画像表示できない。代わりに Claude Desktop などを利用して確認すること。

![AAPL stock chart](./docs/aapl-2y.png)


<details>
<summary>Example: Claude Desktop</summary>

### `claude_desktop_config.json`

```json
{
    "mcpServers": {
        "stack": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "spitson/mcp-create-timeseries-chart"
            ]
        }
    }
}
```

### Screenshot

![GOOG stock chart](./docs/claude_desktop_example_goog.png)

</details>
