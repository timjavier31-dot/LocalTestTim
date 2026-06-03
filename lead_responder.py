import anthropic
import csv
import os
from datetime import datetime

LEADS_FILE = "leads.csv"

def generate_reply(name: str, email: str, message: str) -> str:
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        system=(
            "You are a friendly, professional customer service representative. "
            "Write short, warm, personalized email replies to contact form submissions. "
            "Keep replies under 150 words. Do not use a subject line. Start directly with the greeting."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    f"Write a reply email to this contact form submission:\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Message: {message}"
                ),
            }
        ],
    )

    return response.content[0].text


def save_to_csv(name: str, email: str, message: str, reply: str) -> None:
    file_exists = os.path.isfile(LEADS_FILE)

    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["timestamp", "name", "email", "message", "ai_reply"]
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(),
                "name": name,
                "email": email,
                "message": message,
                "ai_reply": reply,
            }
        )


def process_lead(name: str, email: str, message: str) -> str:
    print(f"\nGenerating reply for {name}...\n")
    reply = generate_reply(name, email, message)
    save_to_csv(name, email, message, reply)
    return reply


if __name__ == "__main__":
    # Sample run — swap these values to test with real data
    sample_name = "Maria Santos"
    sample_email = "maria@example.com"
    sample_message = (
        "Hi, I came across your e-commerce store and I'm interested in your "
        "wholesale pricing. Can you tell me more about your minimum order quantities "
        "and shipping options to the Philippines?"
    )

    reply = process_lead(sample_name, sample_email, sample_message)

    print("=" * 60)
    print("GENERATED REPLY:")
    print("=" * 60)
    print(reply)
    print("=" * 60)
    print(f"\nLead saved to {LEADS_FILE}")
