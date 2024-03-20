import React, { useState } from "react";
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import logo from './logo.svg';
import './App.css';
import MessageList from './Components/Message/Message';

function App() {
  const [messages, setMessages] = useState([]);

  return (
    <>
      <MessageList messages={messages} setMessages={setMessages}></MessageList>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <App />
  </>
);

reportWebVitals();
