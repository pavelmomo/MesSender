import React, { useState } from "react";
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import MessageList from './Components/Message/MessageList';
import MessageAdd from './Components/Message/MessageAdd';

function App() {

  const [messages, setMessages] = useState([]);

  return (
    <div className="app">
      <MessageList messages={messages} setMessages={setMessages}></MessageList>
      <MessageAdd messages={messages} setMessages={setMessages}></MessageAdd>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <>
    <App />
  </>
);

reportWebVitals();
