# TalentScout Hiring Assistant

## Project Overview
TalentScout Hiring Assistant is a simple AI-based chatbot built using Python and Streamlit.
It helps in initial candidate screening by collecting basic details and asking technical
questions based on the candidate’s selected tech stack.

The chatbot works step by step like a real hiring assistant and focuses on clean user
interaction and structured data collection.

---

## Features
- Chatbot-style user interface using Streamlit
- Collects candidate details step by step
- Job role selection using dropdown with manual option
- Experience selection using dropdown (scroll selection)
- Location selection with auto-suggest and manual typing
- Tech stack selection using multi-select with manual fallback
- Technical questions generated using a local LLM (LLaMA via Ollama)
- Questions asked one by one
- Skip question option (stored as N/A)
- Exit keywords supported (bye, exit, quit)
- Candidate responses stored in JSON file
- Thank-you email sent after completion or exit
- No paid APIs used

---

## Technologies Used
- Python
- Streamlit
- Ollama (LLaMA 3 – Local LLM API)
- Requests
- SMTP (Gmail)
- JSON
- python-dotenv

---

## How It Works
1. The chatbot greets the candidate.
2. Collects name, email, phone number.
3. Candidate selects experience using dropdown.
4. Candidate selects job role using dropdown or manual input.
5. Candidate selects location using auto-suggest or manual input.
6. Candidate selects tech stack using multi-select or manual input.
7. Chatbot generates technical questions based on the tech stack.
8. Questions are asked one by one.
9. Candidate can answer, skip, or exit anytime.
10. Responses are saved and a thank-you email is sent.

---

## Data Handling
- Candidate data and answers are stored in:
  candidate_responses.json
- Skipped or empty answers are saved as "N/A".
- Each candidate session is stored as a new entry.
- This uses simulated data storage as required.

---

## Email Functionality
- A thank-you email is sent to the candidate after screening.
- Gmail SMTP with App Password is used.
- Email credentials are stored in a .env file.
- The .env file should not be uploaded to GitHub.

---

## How to Run the Project
python -m streamlit run app.py

### Step 1: Install required libraries
```bash
pip install -r requirements.txt

Step 2: Install and start Ollama
ollama pull llama3

Step 3: Run the application
streamlit run app.py

Environment Variables
Create a .env file in the project folder:

EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

Folder Structure:

talentscout-hiring-assistant/
├── app.py
├── requirements.txt
├── README.md
├── candidate_responses.json
└── .env

Notes:
The LLM runs locally using Ollama, so no paid API is required.
Email sending depends on Gmail security settings.
The chatbot performs only initial screening and does not evaluate answers.
The project is designed to be simple, clear, and easy to understand.
------------------------------------------------------------------------------------------
Project Update

This project was enhanced after the initial implementation to make it more practical and closer to a real-world hiring workflow.

The updated version now includes automatic answer evaluation using a local pre-trained Large Language Model (LLaMA 3 via Ollama). Each candidate response is evaluated as either correct or incorrect, and a binary score is assigned (1 for correct, 0 for incorrect).

All candidate information, interview questions, answers, evaluation results, and scores are now stored in a structured SQLite database. This allows recruiters to easily view complete candidate profiles and shortlist candidates based on their responses and scores.

These updates improve the reliability, usability, and real-world applicability of the hiring assistant while keeping the system simple and independent of paid APIs.

