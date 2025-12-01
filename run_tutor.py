import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from calbright_adk.coordinator import tutor  # root agent


APP_NAME = "calbright_ai_tutor"


async def chat_loop(student_id: str):
    session_service = InMemorySessionService()
    runner = Runner(agent=tutor, session_service=session_service, app_name=APP_NAME)

    # Create a fresh ADK session for this user
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=student_id,
    )

    print("\n==============================")
    print("  Calbright AI Tutor (ADK)")
    print("==============================\n")
    print("Type 'exit' to quit.\n")

    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() in {"exit", "quit"}:
            break

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_msg)],
        )

        final_text_output = []

        async for event in runner.run_async(
            session_id=session.id,
            user_id=student_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            clean = (
                                part.text
                                .replace("<string>", "")
                                .replace("</string>", "")
                            )
                            final_text_output.append(clean)

        answer = "\n".join(final_text_output).strip()
        print(f"Tutor: {answer}\n")

    print("Goodbye!")


def main():
    print("Loading FAISS index...")

    student_id = input("\nEnter your CCCID or Calbright email (type anything - future versions will keep track of student interactions): ").strip()
    asyncio.run(chat_loop(student_id))


if __name__ == "__main__":
    main()
