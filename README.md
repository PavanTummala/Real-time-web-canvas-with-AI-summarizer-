
# AI-Powered Collaborative Whiteboard

IntelliDraw is a real-time collaborative whiteboard that combines low-latency multi-user interaction with AI-powered media summarization.

It demonstrates how WebSockets, FastAPI, React.js, and Vision-Language Models (VLMs) can be integrated to enhance collaboration.

---

## ✨ Features

-   **Real-Time Multi-User Collaboration**
    
    Draw or upload images on a shared canvas, instantly synced across participants using WebSockets.
    
-   **AI-Powered Image Summarization**
    
    Uploaded images are processed through an AI pipeline:
    -   **BLIP** (Bootstrapping Language-Image Pretraining) generates natural language captions from images.
    -   **Ollama** (8B LLM, e.g., LLaVA or Llama 3) refines those captions into concise, human-friendly subtitles.
-   **Containerized Deployment**
    
    The full stack runs in Docker with Docker Compose, making it simple to spin up locally or deploy.
    

---

## 🛠 Technology Stack

-   **Backend**
    -   FastAPI (Python)
    -   WebSockets for real-time sync
    -   Hugging Face BLIP for captioning
    -   Ollama for text synthesis
    -   Pillow (PIL) for image handling
-   **Frontend**
    -   React.js
    -   HTML5 `<canvas>` for drawing
    -   WebSocket API for communication
-   **Infrastructure**
    -   Docker & Docker Compose

---



## Project Structure

```
intellidraw/
├── backend/        # FastAPI application
├── frontend/       # React.js application
├── docker-compose.yml # Main orchestration file
└── README.md
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd intellidraw
    ```

2.  **Build and run the services using Docker Compose:**
    ```sh
    docker-compose up --build
    ```

3.  **Access the application:**
    -   The **Frontend** will be available at [http://localhost:3000](http://localhost:3000).
    -   The **Backend API** will be available at [http://localhost:8000/docs](http://localhost:8000/docs) for the Swagger UI.

## Next Steps & Future Enhancements

This project provides a solid foundation. Here's how you can extend it:

1.  **Integrate a Real LLM**:
    -   Replace the mock function in `backend/app/services/llm_service.py` with actual calls to a multimodal LLM API.
    -   You can host an open-source model like LLaVA yourself or use a cloud-based vision API.
2.  **Implement a RAG Pipeline**:
    -   Set up a vector database (e.g., ChromaDB, Weaviate).
    -   Create a script to populate the database with image embeddings of various objects or diagrams.
    -   Modify the `llm_service` to first retrieve relevant examples from the vector DB based on the user's drawing and then pass them as context to the LLM for more accurate analysis.
3.  **Improve Drawing Tools**:
    -   Add features like changing colors, brush sizes, or drawing specific shapes (rectangles, circles).
    -   Implement an "undo" feature.
4.  **User Authentication**:
    -   Add a login system to manage users and perhaps save whiteboards.
5.  **Persistence**:
    -   Save the state of the whiteboard to a database so that it can be reloaded later.
