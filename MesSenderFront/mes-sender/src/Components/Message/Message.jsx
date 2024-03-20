import React, { useState, useEffect } from "react";

function MessageList ({messages, SetMessages})
{

    useEffect(() => {    
        fetch('http://localhost:8000/api/dialogs/1/messages?user_id=1')
        .then(response => response.json()
        .then(data => { 
            console.log(data);
            SetMessages(data);
        }))
        
      },[]);
    

    return (
        <>
          <ul>{messages.map((message) =><li>{message}</li>)}</ul>
        </>
      );
};

export default MessageList;