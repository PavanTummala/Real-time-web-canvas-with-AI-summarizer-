# IntelliDraw - AI-Powered Collaborative Whiteboard

IntelliDraw is a web-based collaborative whiteboard application that uses WebSockets for real-time communication and a machine learning backend to analyze and identify drawings.

This project serves as a template to demonstrate the integration of a modern web stack for real-time applications with AI features.

## Features

- **Real-time Collaboration**: Multiple users can draw on the same canvas and see each other's updates instantly.
- **AI-Powered Drawing Analysis**: Users can request an AI analysis of the current canvas content. The backend uses a (mocked) multimodal LLM to describe the drawing.
- **Containerized**: The entire application stack (frontend and backend) is containerized with Docker for easy setup and deployment.

## Technology Stack

- **Backend**:
  - **Framework**: FastAPI (Python)
  - **WebSockets**: `websockets` library
  - **Image Processing**: OpenCV
  - **AI Service**: Mocked service simulating a call to a multimodal LLM like [LLaVA](https://llava-vl.github.io/).
- **Frontend**:
  - **Framework**: React.js
  - **Canvas Library**: `react-konva` for simplified HTML5 Canvas interactions.
  - **WebSocket Client**: Native Browser WebSocket API.
- **Orchestration**:
  - **Containerization**: Docker & Docker Compose

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
