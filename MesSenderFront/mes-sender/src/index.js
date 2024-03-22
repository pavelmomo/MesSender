import React, { useState } from "react";
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import MessageList from './Components/Message/MessageList';

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
