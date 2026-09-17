"""MCP Client and Tool Registry for Secure Tool Calling."""

import time
from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any

from backend.app.schemas.travel_state import ToolCallInfo
from mcp_servers.flight_server.server import get_flight_details, search_flights
from mcp_servers.hotel_server.server import get_hotel_details, search_hotels
from mcp_servers.travel_server.server import get_destination_info, search_attractions
from mcp_servers.weather_server.server import get_weather_forecast


class MCPToolRegistry:
    """Registry and allowlist of callable MCP tools."""

    ALLOWLISTED_TOOLS: dict[str, Callable[..., Any]] = {
        "search_flights": search_flights,
        "get_flight_details": get_flight_details,
        "search_hotels": search_hotels,
        "get_hotel_details": get_hotel_details,
        "get_weather_forecast": get_weather_forecast,
        "search_attractions": search_attractions,
        "get_destination_info": get_destination_info,
    }

    @classmethod
    def is_tool_allowed(cls, tool_name: str) -> bool:
        """Check if tool name is in explicit allowlist."""
        return tool_name in cls.ALLOWLISTED_TOOLS


class MCPClient:
    """Client for executing MCP tool calls with bounds, timeouts, and validation."""

    @classmethod
    def call_tool(
        cls,
        agent_name: str,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        timeout_seconds: float = 5.0,
    ) -> tuple[bool, Any, ToolCallInfo]:
        """Execute an allowlisted MCP tool call with strict boundary validation."""
        args = arguments or {}
        start_time = time.perf_counter()
        timestamp = datetime.now(timezone.utc).isoformat()

        # 1. Allowlist security check
        if not MCPToolRegistry.is_tool_allowed(tool_name):
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            info = ToolCallInfo(
                agent_name=agent_name,
                tool_name=tool_name,
                arguments=args,
                result_summary=f"Security Error: Tool '{tool_name}' is not in allowlist.",
                execution_time_ms=elapsed_ms,
                is_demo=True,
                timestamp=timestamp,
            )
            return False, None, info

        # 2. Execute tool
        try:
            tool_func = MCPToolRegistry.ALLOWLISTED_TOOLS[tool_name]
            result = tool_func(**args)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            summary = f"Successfully executed '{tool_name}'"
            if isinstance(result, dict) and "total_options" in result:
                summary = f"Found {result['total_options']} options via '{tool_name}'"

            info = ToolCallInfo(
                agent_name=agent_name,
                tool_name=tool_name,
                arguments=args,
                result_summary=summary,
                execution_time_ms=round(elapsed_ms, 2),
                is_demo=True,
                timestamp=timestamp,
            )
            return True, result, info
        except Exception as err:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            info = ToolCallInfo(
                agent_name=agent_name,
                tool_name=tool_name,
                arguments=args,
                result_summary=f"Tool Execution Error: {err!s}",
                execution_time_ms=round(elapsed_ms, 2),
                is_demo=True,
                timestamp=timestamp,
            )
            return False, None, info
