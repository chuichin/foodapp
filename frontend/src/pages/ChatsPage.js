import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import logo from '../images/chatImage.png';
import { fetchChatsData } from '../actions';
import PageContainer from '../containers/PageContainer';
import ChatItem from '../components/ChatItem';
import classes from './ChatsPage.module.css';

const ChatsPage = props => {
  const currentUserEmail =
    props.currentUserEmail || localStorage.getItem('email');

  console.log(props.chats);

  useEffect(() => {
    props.fetchChatsData(currentUserEmail);
  }, []);

  return (
    <PageContainer>
      <div className={classes.pageHeader}>
        <img src={logo} alt="breakfast" className={classes.headerImage} />
        <h2 className={classes.heading}>Messages</h2>
      </div>

      <ul className={classes.chatList}>
        {props.chats.map(chat => (
          <ChatItem
            {...chat}
            key={chat._id}
            receiverEmail={
              currentUserEmail === chat.receiverEmail
                ? chat.senderEmail
                : chat.receiverEmail
            }
          />
        ))}
      </ul>
    </PageContainer>
  );
};

const mapStateToProps = state => {
  return {
    chats: state.chat.chats,
    currentUserEmail: state.email.email,
  };
};

export default connect(mapStateToProps, { fetchChatsData })(ChatsPage);
