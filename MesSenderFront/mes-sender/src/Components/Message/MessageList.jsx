import React, { useEffect, useState } from "react";
import './Message.css';
function MessageList ({messages, setMessages})
{
    const [editFields, setEditFields] = useState([]);

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
                                      if (res.status) 
                                        setMessages(messages.filter(e => e.id !== id))
                                     } )
                         
      };
      async function changeMessageHandle(e, mes_id)
      {
        if (editFields.indexOf(mes_id) === -1)
          setEditFields([...editFields, mes_id]);
        else{
          const new_text = document.getElementById('pole' + mes_id).value;
          const msg_data = {
            id: mes_id,
            text: new_text
          }
          const url = 'http://localhost:8000/api/messages/';
          const result = await fetch(url,
                                    {
                                      method: 'PUT',
                                      headers: {
                                        "Content-Type": "application/json"
                                      },
                                      body: JSON.stringify(msg_data)

                                    }).then(response => response.json(),
                                      error => console.log(error))
                                      .then(res =>{
                                        if (res.status){
                                          const msg = messages.find((e) => e.id === mes_id);
                                          msg.text = new_text;
                                          setEditFields(editFields.filter( (e) => e !== mes_id));
                                        }
                                          
                                       } )

          


        }                 
      };
    
    return (
        <div className="message-list" >
        <h2>Сообщения</h2>
          <ul >{messages.map((message) =>
            <li key={message.id} >
              {(new Date(message.created_at)).toLocaleTimeString() + " - "}
              <input type="text" id={ 'pole' + message.id} disabled={editFields.indexOf(message.id) !== -1 ? false : true} 
                     defaultValue={message.text}></input>
              <input type="button" value="Удалить" onClick={(e) => deleteMessage(message.id)}></input>
              <input type="button" value={ editFields.indexOf(message.id) !== -1  ? "Сохранить" : "Изменить"} 
                     onClick={(e) => changeMessageHandle(e,message.id)}></input>
            </li>)}
          </ul>
        </div>
      );
};

export default MessageList;