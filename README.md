## NormalObjects Creative Complaint Handler (LangChain)
A creative multi-tool AI agent built with LangChain.
This project implements Becma’s Chaos Mode, an autonomous tool-calling agent that resolves fictional complaints about inconsistencies in the “Downside-Up” universe.

## Features

- Custom tool creation using @tool
- Autonomous multi-tool chaining
- Flexible agent behavior (freeform workflow)
- Tool usage tracking and behavior analysis
- Multiple complaint test cases

## Architecture
LLM: OpenAI gpt-4o-mini
Agent Framework: create_agent() (LangChain v1)

Tools:
- consult_demogorgon
- check_hawkins_records
- cast_interdimensional_spell
- gather_party_wisdom

## The agent dynamically decides:

Which tool to call
- In what order
- Whether to chain multiple tools
- How to integrate tool outputs into a final response
