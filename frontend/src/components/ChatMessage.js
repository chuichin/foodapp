import React from 'react';
import moment from 'moment';
import classes from './ChatMessage.module.css';

const ChatMessage = ({ senderEmail, message, createdAt }) => {
  const currentUserEmail = localStorage.getItem('email');

  if (senderEmail === currentUserEmail) {
    return (
      <li className={classes.messageSent}>
        <div className={classes.messageSentContainer}>{message}</div>
        <span className={classes.date}>
          {moment(parseFloat(createdAt)).format('MMMM Do YYYY, h:mm:ss a')}
        </span>
      </li>
    );
  }

  return (
    <li className={classes.messageReceived}>
      <div className={classes.messageReceivedContainer}>{message}</div>
      <span className={classes.date}>
        {moment(parseFloat(createdAt)).format('MMMM Do YYYY, h:mm:ss a')}
      </span>
    </li>
  );
};

export default ChatMessage;
