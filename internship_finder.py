import smtplib
import os
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup
from datetime import datetime

SEARCH_QUERIES = [
    "data analyst intern remote",
    "data analysis intern india",
    "python intern remote",
    "data analyst intern Indore",
    "data analyst intern Vadodara",
    "data analyst intern Bhusawal"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_RESULTS = 10

def google_search(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+") + "+internship"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []
    for g in soup.select("div.tF2Cxc")[:MAX_RESULTS]:
        title = g.select_one("h3")
        link = g.select_one("a")
        summary = g.select_one("div.VwiC3b")

        if title and link:
            jobs.append({
                "title": title.text,
                "summary": summary.text if summary else "Internship role",
                "link": link["href"]
            })
    return jobs

def main():
    all_jobs = []
    for q in SEARCH_QUERIES:
        all_jobs += google_search(q)

    today = datetime.now().strftime("%d %B %Y")

    with open("daily_internships.md", "w", encoding="utf-8") as f:
        f.write(f"# Internship Update – {today}\n\n")
        for i, job in enumerate(all_jobs[:10], 1):
            f.write(f"{i}. **{job['title']}**\n")
            f.write(f"   - {job['summary']}\n")
            f.write(f"   - {job['link']}\n\n")

    print("Done")

main()
def send_email():
    email = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]

    msg = EmailMessage()
    msg["Subject"] = "Daily Internship Update"
    msg["From"] = email
    msg["To"] = email

    with open("daily_internships.md", "r", encoding="utf-8") as f:
        msg.set_content(f.read())

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)

send_email()
