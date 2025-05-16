import json
import re
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()  
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file!")

client = Groq(api_key=GROQ_API_KEY)


def generate_cover_letter_parts(user_job_json: dict) -> tuple:
    user = user_job_json["user"]
    job = user_job_json["job"]

    prompt = f"""
      You are an expert cover letter writer. Based on the following structured user and job information in JSON format, generate three professional and engaging paragraphs of a cover letter: Opening, Body, and Closing .

      1. **Opening Paragraph**:
        In the opening paragraph tell how you learned about the position. You may, for example, know of a job through: Qaddemly website  . 

      2. **Body Paragraph**:
          This paragraph (dosen't exceed 50 words) and gives a summary of your background and critical skills (hard skills) that make you qualified for the position.
          This paragraph can be used to demonstrate your persuasive skills (soft skills).
           

      3. **Closing Paragraph**:
        At the end of the letter (dosen't exceed 50 words) talk about your availability for the job, where you can be contacted, and when you are going to contact the hiring person for an appointment to discuss your application. If you have no contact name you may simply want to indicate your anticipation for a response in this part of the letter. Thank the person to whom you are writing for his/her time and consideration of your application.
      

      **User information:**
      {user}

      **Job information:**
      {job}

      ## Style guideline:
        Avoid overused buzzwords, filler phrases, clichés, and flowery language. Focus on delivering the information in a concise and natural tone without unnecessary embellishments, jargon, or redundant phrases.
      
      ## some strict:
      each paragraph doesn't exceed 40 to 60 words . 
    """

    # Request to Groq API to generate the cover letter
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=600,
    )

    content = response.choices[0].message.content.strip()

    # Split by double newlines (paragraphs)
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # Remove the first line if it's an intro like "Here's a cover letter..."
    if "cover letter" in paragraphs[0].lower():
        paragraphs = paragraphs[1:]

    # Remove any bolded headers like "**Opening Paragraph**"
    cleaned_paragraphs = [re.sub(r"\*\*.*?\*\*", "", p).strip() for p in paragraphs]

    # Ensure we still have exactly 3 paragraphs
    if len(cleaned_paragraphs) != 3:
        raise ValueError("The cleaned cover letter doesn't contain all required sections.")

    # Merge them into one string
    final_text = "\n".join(cleaned_paragraphs)

    return cleaned_paragraphs, final_text

"""
Result for sample Input:

  "I am writing to express my interest in the Senior Full-Stack Developer position at TechInnovate, which I came across on the Qaddemly website. As a seasoned software engineer with a passion for building scalable web applications, I am excited about the opportunity to join your engineering team and contribute to the company's mission of providing innovative productivity tools for remote teams.
  
  With over 5 years of experience in full-stack development, I possess a unique combination of technical skills and soft skills that make me an ideal fit for this role. In my current position as a Senior Software Engineer at Airbnb, I have honed my expertise in designing and implementing features across the entire stack, from database to UI, using modern JavaScript frameworks such as React, Node.js, and TypeScript. I have also developed strong skills in database design and API development, which I believe will serve me well in this position. My experience in mentoring junior developers has also given me a unique perspective on how to effectively communicate technical ideas and collaborate with cross-functional teams. I am confident that my skills, experience, and passion for clean code and user experience make me a strong candidate for this position.
  
  Thank you for considering my application for the Senior Full-Stack Developer position at TechInnovate. I am excited about the opportunity to discuss my qualifications further and learn more about your team's work. I can be reached at emma.wilson@example.com or +1 415 555 0199. I would appreciate the opportunity to schedule an appointment to meet and discuss my application. I look forward to hearing from you soon and learning about the next steps in the process. Thank you again for your time and consideration."

"""


if __name__ == "__main__":
    # Define the path to the JSON input file
    input_file_path = "data/sampleinput.json"

    # Check if file exists
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file '{input_file_path}' not found!")

    # Load the JSON data
    with open(input_file_path, "r", encoding="utf-8") as file:
        user_job_json = json.load(file)

    try:
        # Generate the cover letter
        result, text = generate_cover_letter_parts(user_job_json)

        # Print the generated cover letter
        print("\nGenerated Cover Letter:\n")
        print(result)
        print("text : \n")
        print(text)

    except Exception as e:
        print(f"Error: {e}")
