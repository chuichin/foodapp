import React, { useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { FaChevronLeft, FaPlus, FaPaperPlane, FaRegGrin } from 'react-icons/fa';
import TextareaAutosize from 'react-textarea-autosize';
import Picker from 'emoji-picker-react';
import {
  toggleEmojiPicker,
  fetchSingleChatData,
  onMessageInputChange,
  insertMessage,
} from '../actions';
import socket from '../utils/socket';
import ChatMessage from '../components/ChatMessage';
import classes from './SingleChatPage.module.css';
import chef1 from '../images/chef1.jpg';

const SingleChatPage = props => {
  const { receiverEmail } = props.match.params;

  const currentUserEmail =
    props.currentUserEmail || localStorage.getItem('email');

  const messagesEndRef = useRef();

  useEffect(() => {
    props.fetchSingleChatData(currentUserEmail, receiverEmail);
    socket.on('receiveBroadcast', msg => props.insertMessage(msg));
  }, []);

  useEffect(() => {
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
  }, [props.messages]);

  const onEmojiClick = (e, emojiObject) => {
    const message = `${props.message}${emojiObject.emoji}`;

    props.onMessageInputChange(message);
  };

  const onSendBtnClick = () => {
    const roomID = localStorage.getItem('roomID');

    socket.emit('broadcastMessage', roomID, currentUserEmail, props.message);

    props.onMessageInputChange('');
  };

  return (
    <div className={classes.pageContainer}>
      <div className={classes.pageHeader}>
        <div className={classes.backIconContainer}>
          <Link to="/chats" className={classes.backIcon}>
            <FaChevronLeft />
          </Link>
        </div>
        <div className={classes.imageContainer}>
          <img src={chef1} alt="chef1" className={classes.receiverImage} />
        </div>
        <div className={classes.receiverContainer}>
          <p className={classes.receiverName}>{props.receiverName}</p>
          <p className={classes.status}>Online</p>
        </div>
      </div>

      <ul className={classes.contentContainer}>
        {props.messages.map((message, index) => (
          <ChatMessage key={index} {...message} />
        ))}
        <div ref={messagesEndRef}></div>
      </ul>

      <div className={classes.form}>
        <div className={classes.imageUploadContainer}>
          <input
            type="file"
            id="chatImageUpload"
            className={classes.imageInput}
          />
          <label htmlFor="chatImageUpload" className={classes.inputLabel}>
            <FaPlus className={classes.plusIcon} />
          </label>
        </div>
        <div className={classes.textareaContainer}>
          {props.ui.isEmojiPickerOpen && (
            <Picker
              pickerStyle={{
                position: 'absolute',
                right: '0',
                bottom: '150%',
                maxWidth: '18em',
                maxHeight: '20em',
              }}
              onEmojiClick={onEmojiClick}
            />
          )}
          <TextareaAutosize
            className={classes.textarea}
            minRows="1"
            maxRows="6"
            value={props.message}
            onChange={e => props.onMessageInputChange(e.target.value)}
          />
          <button
            className={classes.btnEmoji}
            onClick={props.toggleEmojiPicker}
          >
            <FaRegGrin />
          </button>
        </div>
        <div className={classes.btnContainer}>
          <button className={classes.chatBtnSubmit} onClick={onSendBtnClick}>
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  );
};

const mapStateToProps = state => {
  return {
    ui: state.ui,
    messages: state.message.messages,
    message: state.message.message,
    receiverName: state.message.receiverName,
    currentUserEmail: state.email.currentUserEmail,
  };
};

export default connect(mapStateToProps, {
  toggleEmojiPicker,
  fetchSingleChatData,
  onMessageInputChange,
  insertMessage,
})(SingleChatPage);
