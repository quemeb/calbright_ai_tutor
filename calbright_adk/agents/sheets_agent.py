from google.adk.agents import Agent
from calbright_adk.tools.course_rag import course_rag

sheets_agent = Agent(
    name="sheets_tutor",
    model="gemini-2.5-flash-lite",
    description="Google Sheets / Spreadsheet specialist tutor.",
    instruction=(
        "You are a Google Sheets tutor for adult learners in Calbright's "
        "Data Analytics program.\n\n"
        "SCOPE:\n"
        "- ONLY answer spreadsheet questions: formulas, functions, pivot tables, "
        "  data cleaning, filters, formatting.\n"
        "- If not Sheets-related, say it is outside your scope.\n\n"
        "TOOL USAGE:\n"
        "- Call course_rag(module='Sheets') for authenticated course context.\n\n"
        "STYLE:\n"
        "- Medium-length explanations with concrete examples."
    ),
    tools=[course_rag],
)
