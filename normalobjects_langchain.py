import random
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import ToolMessage



@tool
def consult_demogorgon(complaint: str) -> str:
    """Get the Demogorgon's perspective on a complaint about inconsistencies."""
    responses = [
        f"The Demogorgon tilts its head at '{complaint}'. Perhaps you're assuming reality should be consistent?",
        f"The Demogorgon clicks approvingly. It suggests time flows sideways where the complaint originated: '{complaint}'.",
        f"The Demogorgon seems distracted by snacks. It communicates that 'consistency' is an Earth-only hobby: '{complaint}'.",
    ]
    return random.choice(responses)


@tool
def check_hawkins_records(query: str) -> str:
    """Search Hawkins historical records for information."""
    records = {
        "portal": "Records show portals have opened on various dates with no clear pattern. Weather, electromagnetic activity, and unknown factors seem involved.",
        "monsters": "Historical records indicate creatures behave differently based on environmental factors, time of day, and proximity to certain individuals.",
        "psychics": "Records show psychic abilities vary greatly. Some can move objects but not see visions; others see visions but can't move objects.",
        "electricity": "Hawkins has a history of electrical anomalies. Records suggest a connection between interdimensional activity and electromagnetic fields.",
    }

    q = query.lower()
    for key, value in records.items():
        if key in q:
            return value

    return f"Records don't contain specific information about '{query}', but they note many unexplained events over the years."


@tool
def cast_interdimensional_spell(problem: str, creativity_level: str = "medium") -> str:
    """Suggest a creative interdimensional spell to fix a problem."""
    creativity_multiplier = {"low": 1, "medium": 2, "high": 3}.get(creativity_level, 2)

    spells = [
        f"Chant 'Becma Becma Becma' three times while holding a Walkman to recalibrate frequencies around: {problem}",
        f"Draw a salt circle, place a compass in the center, and wait for the needle to twitch—then address: {problem}",
        f"Play 'Running Up That Hill' backwards at the exact location of the glitch to induce temporal resonance for: {problem}",
        f"Gather a lighter, a compass, and something personal; form a triangle and focus intensely on: {problem}",
    ]

    selected = random.sample(spells, k=min(creativity_multiplier, len(spells)))
    return "\n".join(selected)


@tool
def gather_party_wisdom(question: str) -> str:
    """Ask the D&D party for their collective wisdom."""
    party_responses = {
        "portal": "Mike: 'Portals open near strong emotional events or electromagnetic disturbances.' Dustin: 'Also tied to Mind Flayer patterns.'",
        "monsters": "Lucas: 'They’re territorial but opportunistic.' Will: 'They sense fear and strong emotions—behavior shifts with the vibe.'",
        "psychics": "Mike: 'Powers connect to emotional state.' Dustin: 'Physical and mental energy limit what they can do.'",
        "electricity": "Lucas: 'Interdimensional stuff interferes with power lines.' Dustin: 'But it also creates weird feedback loops.'",
    }

    q = question.lower()
    for key, response in party_responses.items():
        if key in q:
            return response

    return "The party huddles. Mike: 'Tough one.' Dustin: 'We need more info.' Lucas: 'Let’s list what we know.' Will: 'Consult other sources?'"


def main() -> None:
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    agent = create_agent(
        model=llm,
        tools=[
            consult_demogorgon,
            check_hawkins_records,
            cast_interdimensional_spell,
            gather_party_wisdom,
        ],
        system_prompt=(
            "You are Becma's Chaos Mode at the Downside-Up Complaint Bureau.\n"
            "Goal: resolve complaints creatively and entertainingly.\n"
            "Use tools freely in any order. You may call multiple tools.\n"
            "Always end with a clear, playful 'Resolution' for the complainant."
        ),
        debug=True,
        name="becma-chaos-mode",
    )

    complaints = [
        "Why do demogorgons sometimes eat people and sometimes don't?",
        "The portal opens on different days—is there a schedule?",
        "Why can some psychics see the Downside Up and others can't?",
        "Why do creatures and power lines react so strangely together?",
    ]

    from langchain_core.messages import ToolMessage

    tool_counts = {
        "consult_demogorgon": 0,
        "check_hawkins_records": 0,
        "cast_interdimensional_spell": 0,
        "gather_party_wisdom": 0,
    }

    tool_sequence = []

    def handle_complaint(complaint: str) -> None:
        print("\n" + "=" * 60)
        print("COMPLAINT:", complaint)
        print("=" * 60)

        result = agent.invoke(
            {"messages": [("user", f"Complaint: {complaint}")]}
        )

        # Track tool usage
        for msg in result["messages"]:
            if isinstance(msg, ToolMessage):
                tool_sequence.append(msg.name)
                if msg.name in tool_counts:
                    tool_counts[msg.name] += 1

        final_text = result["messages"][-1].content
        print("\nRESPONSE:\n", final_text)

    print("\nTesting agent with sample complaints...\n")

    for complaint in complaints[:3]:
        handle_complaint(complaint)

    print("\n=== Tool Usage Analysis ===")
    total_calls = sum(tool_counts.values())
    most_used = max(tool_counts.items(), key=lambda x: x[1])[0] if total_calls else None

    print("Total tool calls:", total_calls)
    print("Tool counts:", tool_counts)
    print("Most used tool:", most_used)
    print("Tool sequence:", " -> ".join(tool_sequence) if tool_sequence else "(no tools called)")


if __name__ == "__main__":
    main()
