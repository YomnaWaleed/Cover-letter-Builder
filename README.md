# AI Cover Letter Generator

A FastAPI application that generates professional cover letters using Groq's LLM API.

## Features

- Generates 3-part cover letters (opening, body, closing)
- Processes user profiles and job descriptions in JSON format
- Uses LLaMA 3 (via Groq) for high-quality text generation
- FastAPI backend for easy integration

## Requirements

- Python 3.8+
- Groq API key (free tier available)

## Installation
    1- clone Reposirtory
```bash 
      git clone https://github.com/YomnaWaleed/Cover-letter-Builder.git
      cd Cover-letter-Builder
    
```

    2- Create and activate a virtual environment

    3- Install dependencies
  
```bash pip install -r requirements.txt ```

    4- Create a .env file and add your Groq API key


## Usage 
  Running the API
    Start the FastAPI server:
    ```bash uvicorn main:app --reload ```
   