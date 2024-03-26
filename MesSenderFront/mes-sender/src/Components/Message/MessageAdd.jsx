import React, { useEffect } from "react";
import './Message.css';

function MessageAdd ({messages, setMessages})
{

  function handleSubmit(e)
  {
    e.preventDefault();
    addMessage(document.getElementById("MessageText").value);
    
  }

    useEffect(() => {    
        fetch('http://localhost:8000/api/dialogs/1/messages?user_id=1')
        .then(response => response.json())
        .then(
          data => { 
            setMessages(data);
          },
          error => console.log(error)
          )},[]);

      async function addMessage(text)
      {
        
        let newMessage = {
          dialog_id: 1,
          user_id: 1,
          text: String(text)
        }
        
        const url = 'http://localhost:8000/api/messages/';
        const result = await fetch(url,
                                  {
                                    method: 'POST',
                                    headers: {
                                      "Content-Type": "application/json"
                                    },
                                    body: JSON.stringify(newMessage),
                                  }).then(response => response.json(),
                                    error => console.log(error))
                                    .then(res =>{
                                      if (res.status){
                                        newMessage.created_at = res.created_at;
                                        newMessage.id = res.id;
                                        setMessages(messages = [...messages, newMessage]);
                                        document.getElementById("MessageText").value = "";
                                      }
                                        
                                    });
                                      
                         
      };
    
    return (
        <div className="message-add">
        <h4>Добавить сообщение</h4>
          <form onSubmit={(e) => handleSubmit(e)}>
            <input id="MessageText" ></input>
            <input type="submit" value="Добавить" ></input>
          </form>
        </div>
      );
};

export default MessageAdd;