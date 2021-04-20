const initialState = {
  chats: [],
  currentChat: '',
};

const chatReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_CHATS':
      return { ...state, chats: action.payload };
    case 'SET_CURRENTCHAT':
      return { ...state, currentChat: action.payload };
    default:
      return state;
  }
};

export default chatReducer;
