import axios from 'axios';
import socket from '../utils/socket';

export const toggleNav = () => {
  return { type: 'TOGGLE_NAV' };
};

export const toggleEmojiPicker = () => {
  return { type: 'TOGGLE_EMOJI_PICKER' };
};

export const onEmailChange = email => {
  return {
    type: 'EMAIL_CHANGE',
    payload: email,
  };
};

export const setCurrentUserEmail = email => {
  return { type: 'SET_CURRENTUSER_EMAIL', payload: email };
};

export const fetchChatsData = email => async dispatch => {
  try {
    dispatch({ type: 'START_LOADING' });

    const response = await axios.get(
      `http://localhost:8000/api/v1/chats?email=${email}`
    );

    const { chats } = response.data;

    const roomIDs = chats.map(chat => chat.roomID);

    const emails = chats.map(chat => {
      if (chat.senderEmail === email) {
        return chat.receiverEmail;
      } else {
        return chat.senderEmail;
      }
    });

    const messagesResponses = await Promise.all(
      roomIDs.map(id =>
        axios.get(`http://localhost:8000/api/v1/messages?roomID=${id}`)
      )
    );

    const namesResponses = await Promise.all(
      emails.map(el => axios.get(`http://localhost:8000/api/v1/users/${el}`))
    );

    const messages = messagesResponses.map(
      res => res.data.messages[res.data.messages.length - 1]
    );

    const names = namesResponses.map(res => res.data.user.name);

    chats.forEach((chat, index) => {
      chat.receiverName = names[index];

      if (messages[index]) {
        chat.lastMessage = messages[index].message;
        chat.lastMessageDate = messages[index].createdAt;
      }
    });

    dispatch({ type: 'SET_CHATS', payload: chats });
    dispatch({ type: 'STOP_LOADING' });
  } catch (err) {
    console.log(err);
    //error handling
    dispatch({ type: 'SET_ERROR' });
  }
};

export const fetchSingleChatData = (
  currentUserEmail,
  receiverEmail
) => async dispatch => {
  try {
    dispatch({ type: 'START_LOADING' });

    socket.emit('startChat', currentUserEmail, receiverEmail);

    socket.on('sendRoomID', roomID => {
      localStorage.setItem('roomID', roomID);
    });

    const response = await axios.get(
      `http://localhost:8000/api/v1/users/${receiverEmail}`
    );

    const { name } = response.data.user;

    dispatch({ type: 'SET_RECEIVER_NAME', payload: name });

    socket.on('loadMessages', messages => {
      dispatch({ type: 'FETCH_MESSAGES', payload: messages });
      dispatch({ type: 'STOP_LOADING' });
    });
  } catch (err) {
    console.log(err);
    dispatch({ type: 'SET_ERROR' });
  }
};

export const onMessageInputChange = message => {
  return { type: 'INPUT_MESSAGE_CHANGE', payload: message };
};

export const insertMessage = message => {
  return { type: 'INSERT_MESSAGE', payload: message };
};
