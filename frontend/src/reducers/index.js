import { combineReducers } from 'redux';
import uiReducer from './uiReducer';
import chatReducer from './chatReducer';
import messageReducer from './messageReducer';

const initialState = {
  email: '',
  currentUserEmail: '',
};

const emailReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'EMAIL_CHANGE':
      return { ...state, email: action.payload };
    case 'SET_CURRENTUSER_EMAIL':
      return { ...state, currentUserEmail: action.payload };
    default:
      return state;
  }
};

export default combineReducers({
  ui: uiReducer,
  email: emailReducer,
  chat: chatReducer,
  message: messageReducer,
});
