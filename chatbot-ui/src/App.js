import React, { useState } from "react";
import axios from "axios";
import { TextField, Button, Box, Typography, Paper } from "@mui/material";
import "./App.css";  // You can still use custom styles here

function App() {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  // Function to handle sending the input to Flask backend
  const sendMessage = async () => {
    if (!userInput) return;  // Don't send if input is empty

    // Add user input to chat history
    const newChatHistory = [...chatHistory, { role: "user", message: userInput }];
    setChatHistory(newChatHistory);
    setUserInput(""); // Clear the input field

    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        user_input: userInput,
      });

      const chatbotResponse = response.data.response;

      // Add chatbot response to chat history after the user message
      setChatHistory([
        ...newChatHistory,
        { role: "assistant", message: chatbotResponse },
      ]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory([
        ...newChatHistory,
        { role: "assistant", message: "Sorry, something went wrong!" },
      ]);
    }
  };

  return (
    <Box className="App" sx={{ display: "flex", flexDirection: "column", alignItems: "center", height: "100vh", padding: 3 }}>
      <Box
        className="chat-box"
        sx={{
          width: "100%",
          maxWidth: 600,
          height: "70vh",
          overflowY: "scroll",
          border: "1px solid #ccc",
          borderRadius: 2,
          padding: 2,
          backgroundColor: "#fff",
          marginBottom: 3,
          boxShadow: 2,
          scrollbarWidth:'none'
        }}
      >
        {chatHistory.map((chat, index) => (
          <Paper key={index} sx={{ padding: 2, marginBottom: 1, backgroundColor: chat.role === "user" ? "#cce5ff" : "#e2e3e5",overflowY:'scroll',scrollbarWidth:'none' }}>
            <Typography variant="body2" component="span" sx={{ fontWeight: "bold", marginRight: 1 }}>
              {chat.role === "user" ? "You" : "Zeta's AI Twin"}:
            </Typography>
            <Typography variant="body2" component="span">{chat.message}</Typography>
          </Paper>
        ))}
      </Box>

      <Box className="input-container" sx={{ display: "flex", justifyContent: "space-between", width: "100%", maxWidth: 600}}>
        <TextField
          label="Ask me anything..."
          variant="outlined"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          fullWidth
          sx={{ marginRight: 2 }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={sendMessage}
          sx={{ height: "100%" }}
        >
          Send
        </Button>
      </Box>
    </Box>
  );
}

export default App;
