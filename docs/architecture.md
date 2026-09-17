# TravelPilot AI - Architecture Specification

## Overview
This document details the system design, agent hierarchy, data flow, state management, and orchestration design for TravelPilot AI.

## Core Design Principles
1. **Free-First & Deterministic Core**: Primary LLM runs on Groq's free tier. Arithmetic and strict constraints are calculated deterministically in Python.
2. **Stateful Graph Orchestration**: LangGraph manages workflows as explicit state graphs with conditional dynamic routing.
3. **Model Context Protocol (MCP)**: Tools communicate via MCP standard protocol.
4. **Human-in-the-Loop Safety**: Workflows pause at critical evaluation nodes for user approval/feedback before graph resumption.
