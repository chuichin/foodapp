import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { setCurrentUserEmail } from '../actions';
import { onEmailChange } from '../actions';

const LoginPage = props => {
  const onLinkClick = () => {
    localStorage.setItem('email', props.email.email);
    props.setCurrentUserEmail(props.email.email);
  };

  return (
    <>
      <input
        type="text"
        value={props.email.email}
        onChange={e => props.onEmailChange(e.target.value)}
      />
      <Link to="/chats" onClick={onLinkClick}>
        Login
      </Link>
    </>
  );
};

const mapStateToProps = state => {
  return {
    email: state.email,
  };
};

export default connect(mapStateToProps, { onEmailChange, setCurrentUserEmail })(
  LoginPage
);
