# Medical_Chatbot

## End-to-End Medical Chatbot using Generative AI (RAG, OpenAI,...)

### NOTE ::
This LLM is neither completely fine-tuned, nor there are enough resources in the Vector DB yet to get perfect responses. This is just a prototype project, so, please don't mind any incorrect responses or responses with special characters.

### STEPS :

Clone the repository

```bash
Project repo: https://github.com/dubekeshav/Medical_Chatbot.git
```

#### STEP 1 : Create a conda environment after opening the repository

```bash
conda create -n medical_chatbot python==3.13.2 -y
```

```bash
conda activate medical_chatbot
```

#### STEP 2 : Install the requirements

Before installing the requirements, make sure CMake is install in your PC

```bash
pip install -r requirements.txt
```

#### STEP 3 : Environment variables intialization'

Create a .env file in the project folder and add the pinecone api key (PINECONE_API_KEY), and, hugging face access token (HUGGING_FACE_ACCESS_TOKEN).

#### STEP 4 : Start the application

Make sure you are in the project home directory, and just run the following command to run the application :

```{python}
python run app.py
```