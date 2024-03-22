import React, { useEffect } from "react";

function MessageList ({messages, setMessages})
{

    useEffect(() => {    
        fetch('http://localhost:8000/api/dialogs/1/messages?user_id=1')
        .then(response => response.json())
        .then(
          data => { 
            setMessages(data);
          },
          error => console.log(error)
          )},[]);

      async function deleteMessage(id)
      {
        const url = 'http://localhost:8000/api/messages/' + id;
        const result = await fetch(url,
                                  {
                                    method: 'DELETE'
                                  }).then(response => response.json(),
                                    error => console.log(error))
                                    .then(res =>{
                                      if (res) 
                                        setMessages(messages.filter(e => e.id !== id))
                                     } )
                         
      };
    
    return (
        <>
        <h2>Сообщения</h2>
          <ul>{messages.map((message) =>
            <li key={message.user_id}>Пользователь {message.user_id}: {message.text} 
              <input type="button" value="Удалить" onClick={() => deleteMessage(message.user_id)}></input>
            </li>)}
          </ul>
        </>
      );
};

export default MessageList;