import React, { useState, useRef, useEffect } from 'react';
import { Stage, Layer, Line } from 'react-konva';
import { v4 as uuidv4 } from 'uuid';

const WEBSOCKET_URL = "ws://localhost:8000/ws/" + Date.now(); // Unique ID for this client
const API_URL = "http://localhost:8000/analyze";

const Whiteboard = () => {
    const [lines, setLines] = useState([]);
    const [analysisResult, setAnalysisResult] = useState(null);
    const isDrawing = useRef(false);
    const stageRef = useRef(null);
    const ws = useRef(null);

    useEffect(() => {
        // Initialize WebSocket connection
        ws.current = new WebSocket(WEBSOCKET_URL);

        ws.current.onopen = () => console.log("WebSocket connected!");
        ws.current.onclose = () => console.log("WebSocket disconnected.");

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'drawing') {
                setLines(prevLines => [...prevLines, data.payload]);
            } else if (data.type === 'analysis_result') {
                setAnalysisResult(data.payload);
            }
        };

        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, []);

    const handleMouseDown = (e) => {
        isDrawing.current = true;
        const pos = e.target.getStage().getPointerPosition();
        const newLine = { id: uuidv4(), points: [pos.x, pos.y] };
        setLines([...lines, newLine]);
    };

    const handleMouseMove = (e) => {
        if (!isDrawing.current) return;

        const stage = e.target.getStage();
        const point = stage.getPointerPosition();
        let lastLine = lines[lines.length - 1];

        // Add new points to the current line
        lastLine.points = lastLine.points.concat([point.x, point.y]);

        // Replace last line
        const newLines = lines.slice(0, -1).concat(lastLine);
        setLines(newLines);

        // Broadcast the new line segment
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'drawing', payload: lastLine }));
        }
    };

    const handleMouseUp = () => {
        isDrawing.current = false;
    };

    const handleAnalyzeClick = async () => {
        const dataURL = stageRef.current.toDataURL();
        setAnalysisResult({ description: "Analyzing..." });
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ imageDataUrl: dataURL }),
            });
            if (!response.ok) {
                throw new Error("Failed to get analysis from server.");
            }
            // The result will be broadcasted via WebSocket to all clients,
            // including this one, so we don't need to handle the response here.
        } catch (error) {
            console.error("Analysis error:", error);
            setAnalysisResult({ description: `Error: ${error.message}` });
        }
    };

    const handleClearClick = () => {
        setLines([]);
        setAnalysisResult(null);
        // In a real app, you might want to broadcast a 'clear' event too
    };

    return (
        <div>
            <div className="controls">
                <button onClick={handleAnalyzeClick}>Analyze Drawing</button>
                <button onClick={handleClearClick}>Clear</button>
            </div>
            <div className="whiteboard-container">
                <Stage
                    width={800}
                    height={600}
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                    ref={stageRef}
                    style={{ backgroundColor: 'white' }}
                >
                    <Layer>
                        {lines.map((line) => (
                            <Line
                                key={line.id}
                                points={line.points}
                                stroke="#000"
                                strokeWidth={5}
                                tension={0.5}
                                lineCap="round"
                            />
                        ))}
                    </Layer>
                </Stage>
            </div>
            {analysisResult && (
                <div className="analysis-box">
                    <h3>AI Analysis:</h3>
                    <p>{analysisResult.description}</p>
                    {analysisResult.tags && <p><strong>Tags:</strong> {analysisResult.tags.join(', ')}</p>}
                </div>
            )}
        </div>
    );
};

export default Whiteboard;
