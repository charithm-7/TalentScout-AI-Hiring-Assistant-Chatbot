import streamlit as st
import requests
import json
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()


st.title("TalentScout Hiring Assistant")


# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
def generate_questions_with_llm(skill):
    prompt = (
        f"Generate exactly 3 interview questions for {skill}. "
        f"Return ONLY the questions. "
        f"No explanations. No headings. No extra text. "
        f"Each question must be on a new line and end with a question mark."
    )

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload
    )

    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "unable to Generate questions at this time"

    
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

def save_responses(candidate_data, answers):
    record = {
        "timestamp": datetime.now().isoformat(),
        "candidate_details": candidate_data,
        "answers": answers
    }

    try:
        with open("candidate_responses.json", "r") as file:
            content = file.read().strip()
            if content:
                existing_data = json.loads(content)
            else:
                existing_data = []
    except FileNotFoundError:
        existing_data = []

    existing_data.append(record)

    with open("candidate_responses.json", "w") as file:
        json.dump(existing_data, file, indent=4)

def check_exit(user_input):
    if not user_input:
        return False
    return user_input.strip().lower() in ["bye", "exit", "quit"]

def send_thank_you_email(to_email, candidate_name):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials not loaded")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = "Thank you for applying – TalentScout"
        msg["From"] = sender_email
        msg["To"] = to_email

        msg.set_content(
            f"""Hello {candidate_name},

Thank you for applying through TalentScout.

We have received your details and responses.
Our recruitment team will review your profile and contact you if there is a match.

Best regards,
TalentScout Hiring Team
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

    except Exception as e:
        print("Email sending failed:", e)




# Step 0: Greeting
if st.session_state.step == 0:
    st.write("Hello! I am the TalentScout Hiring Assistant.")
    st.write("I will ask you a few questions for initial screening.")
    if st.button("Start"):
        st.session_state.step = 1


# Step 1: Name
elif st.session_state.step == 1:
    name = st.text_input("May I know your full name?")
    if st.button("Next"):
        if name:
            st.session_state.data["name"] = name
            st.session_state.step = 2
        else:
            st.warning("Please enter your name.")


# Step 2: Email
elif st.session_state.step == 2:
    email = st.text_input("Please enter your email address.")
    if st.button("Next"):
        if email:
            st.session_state.data["email"] = email
            st.session_state.step = 3
        else:
            st.warning("Please enter your email.")


# Step 3: Phone
elif st.session_state.step == 3:
    phone = st.text_input("Please enter your phone number.")
    if st.button("Next"):
        if phone:
            st.session_state.data["phone"] = phone
            st.session_state.step = 4
        else:
            st.warning("Please enter your phone number.")


# Step 4: Experience
elif st.session_state.step == 4:

    experience_options = [
        "0 (Fresher)",
        "1 year",
        "2 years",
        "3 years",
        "4 years",
        "5 years",
        "6–10 years",
        "10+ years"
    ]

    experience = st.selectbox(
        "How many years of experience do you have?",
        experience_options
    )

    if st.button("Next"):
        st.session_state.data["experience"] = experience
        st.session_state.step = 5



# Step 5: Desired Position
elif st.session_state.step == 5:

    roles = [
        "AI/ML Intern",
        "Data Science Intern",
        "Software Developer Intern",
        "Backend Developer Intern",
        "Frontend Developer Intern",
        "Full Stack Developer Intern",
        "Other (Type manually)"
    ]

    selected_role = st.selectbox(
        "Which role are you applying for?",
        roles
    )

    if selected_role == "Other (Type manually)":
        position = st.text_input("Please type the role you are applying for")
    else:
        position = selected_role

    if st.button("Next"):
        if position:
            st.session_state.data["position"] = position
            st.session_state.step = 6
        else:
            st.warning("Please select or type a role.")



# Step 6: Location
elif st.session_state.step == 6:

    cities = [
        "Bengaluru",
        "Hyderabad",
        "Chennai",
        "Mumbai",
        "Pune",
        "Delhi",
        "Noida",
        "Gurgaon",
        "Kolkata",
        "Ahmedabad",
        "Other (Type manually)"
    ]

    selected_city = st.selectbox(
        "Where are you currently located?",
        cities
    )

    if selected_city == "Other (Type manually)":
        location = st.text_input("Please type your city name")
    else:
        location = selected_city

    if st.button("Next"):
        if location:
            st.session_state.data["location"] = location
            st.session_state.step = 7
        else:
            st.warning("Please enter your location.")



# Step 7: Tech Stack
elif st.session_state.step == 7:

    known_tech = [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript",
        "Django",
        "Flask",
        "React",
        "Node.js",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "AWS",
        "Docker",
        "TensorFlow",
        "PyTorch"
    ]

    selected_tech = st.multiselect(
        "Select your tech stack (you can choose multiple)",
        known_tech
    )

    custom_tech = st.text_input(
        "If your skill is not listed, type it here (comma separated)"
    )

    if st.button("Next"):
        final_tech = selected_tech.copy()

        if custom_tech:
            custom_list = [t.strip() for t in custom_tech.split(",") if t.strip()]
            final_tech.extend(custom_list)

        if final_tech:
            # Store as comma-separated string (for LLM use)
            st.session_state.data["tech_stack"] = ", ".join(final_tech)
            st.session_state.step = 8
        else:
            st.warning("Please select or enter at least one skill.")



# Step 8 Technical Questions
elif st.session_state.step == 8:

    # Generate questions ONLY ONCE
    if not st.session_state.questions:
        skills = st.session_state.data["tech_stack"].split(",")

        for skill in skills:
            skill = skill.strip()
            if skill:
                llm_output = generate_questions_with_llm(skill)

                for line in llm_output.split("\n"):
                    line = line.strip()
                    if line.endswith("?"):
                        st.session_state.questions.append(line)

    # If questions are remaining
    if st.session_state.current_q < len(st.session_state.questions):

        question = st.session_state.questions[st.session_state.current_q]
        st.write(f"**{question}**")

        with st.form(key=f"form_{st.session_state.current_q}"):

            answer = st.text_area("Your answer:")

            col1, col2 = st.columns(2)
            next_clicked = col1.form_submit_button("Next Question")
            skip_clicked = col2.form_submit_button("Skip Question")

            # EXIT HANDLING FIRST
            if next_clicked and check_exit(answer):
                save_responses(
                    st.session_state.data,
                    st.session_state.answers
                )
                send_thank_you_email(
                    st.session_state.data["email"],
                    st.session_state.data["name"]
                )
                st.success("Thank you for your time. The screening has been ended.")
                st.stop()

            # NEXT QUESTION (with answer or N/A)
            if next_clicked:
                st.session_state.answers[question] = (
                    answer if answer.strip() else "N/A"
                )
                st.session_state.current_q += 1

            # SKIP QUESTION (force N/A)
            if skip_clicked:
                st.session_state.answers[question] = "N/A"
                st.session_state.current_q += 1

    # If all questions are completed
    else:
        save_responses(
            st.session_state.data,
            st.session_state.answers
        )
        send_thank_you_email(
            st.session_state.data["email"],
            st.session_state.data["name"]
        )
        st.success("Thank you! Screening completed.")
        st.write("Our team will contact you soon.")







