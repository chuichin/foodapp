import React from 'react';
import moment from 'moment';
import { Link } from 'react-router-dom';
import classes from './ChatItem.module.css';
import chef1 from '../images/chef1.jpg';

const ChatItem = ({
  receiverName,
  lastMessage,
  lastMessageDate,
  receiverEmail,
}) => {
  return (
    <li className={classes.chatItem}>
      <Link to={`/chats/${receiverEmail}`} className={classes.chatItemLink}>
        <img src={chef1} alt={receiverName} className={classes.chatItemImage} />
        <div className={classes.messageContainer}>
          <p className={classes.chefName}>{receiverName}</p>
          <p className={classes.message}>{lastMessage}</p>
        </div>
        <div className={classes.detailContainer}>
          <p className={classes.date}>
            {lastMessageDate &&
              moment(parseFloat(lastMessageDate)).format('MMM Do YY')}
          </p>
          <div className={classes.notification}>4</div>
        </div>
        <span className={classes.underline}></span>
      </Link>
    </li>
  );
};

export default ChatItem;
