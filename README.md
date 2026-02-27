# 📸 WanderLens: Multimodal Agentic RAG Travel Assistant

WanderLens is an agentic AI travel orchestrator that transforms un-geotagged images into actionable travel itineraries. 

By combining **Google Vertex AI** for multimodal embeddings, **Elasticsearch** for hybrid vector search, and **Gemini 1.5 Pro** for spatial reasoning and synthesis, WanderLens bridges the gap between visual inspiration and concrete travel logistics.

## 🏗️ Architecture Stack
* **Frontend/Orchestration:** Streamlit (Python)
* **Embedding Model:** Google Vertex AI Multimodal Embeddings (`multimodalembedding`)
* **Vector Store:** Elasticsearch 9.x (Elastic Cloud)
* **LLM / Reasoning Engine:** Gemini 1.5 Pro
* **External APIs:** Amadeus (Flights), Google Maps (Routes)
* **Deployment:** Google Cloud Run

---

## ⚙️ Prerequisites

Before running the application, ensure you have active accounts and API keys for the following services:
1. **Google Cloud Platform (GCP):** Project ID, Vertex AI API enabled.
2. **Elastic Cloud:** Deployment URL and API Key (Index configured for 1408-dimensional dense vectors).
3. **Amadeus for Developers:** API Key and Secret.
4. **Google Maps Platform:** Distance Matrix API enabled.

---

## 💻 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/wanderlens.git](https://github.com/your-username/wanderlens.git)
   cd wanderlens
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Configure Environment Variables:
   Copy the example environment file and fill in your actual API keys.
   ```bash
   cp .env.example .env
  Note: Never commit your .env file to version control.
5. Authenticate with Google Cloud:
   ```bash
  gcloud auth application-default login
   ```
6. Run the app locally:
   ```bash
   streamlit run app.py
   ```
---
## 🚀 Deployment to Google Cloud Run
This application is designed to be containerized and deployed seamlessly to Google Cloud Run.

1. Create a Dockerfile in the root directory:
   ``` bash
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8080
 
   CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
   ```
2. Build and Submit the Container to Google Container Registry (GCR):
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_GCP_PROJECT_ID/wanderlens
   ```
3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy wanderlens \
     --image gcr.io/YOUR_GCP_PROJECT_ID/wanderlens \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GCP_PROJECT_ID=your-project-id,GCP_LOCATION=us-central1,ES_URL=your-es-url,ES_API_KEY=your-es-key,AMADEUS_CLIENT_ID=your-amadeus-id,AMADEUS_CLIENT_SECRET=your-amadeus-secret,GMAPS_API_KEY=your-gmaps-key
(Alternatively, use Google Cloud Secret Manager for handling these environment variables in production).

---

## 🧠 Core  Pattern
Unlike standard tool-use where an LLM blindly selects an API, WanderLens implements a spatial reasoning orchestrator. The Python backend retrieves the landmark's coordinates from Elasticsearch and pre-calculates distance vectors before prompting Gemini.

If the user is within a driveable radius, it routes to Google Maps; if they are across the globe, it routes to Amadeus. This reduces LLM hallucinations and API cost overhead.

  
