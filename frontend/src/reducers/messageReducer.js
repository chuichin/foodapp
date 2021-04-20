const initialState = {
  messages: [],
  message: '',
  receiverName: '',
};

const messageReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_MESSAGES':
      return { ...state, messages: action.payload };
    case 'INPUT_MESSAGE_CHANGE':
      return { ...state, message: action.payload };
    case 'SET_RECEIVER_NAME':
      return { ...state, receiverName: action.payload };
    case 'INSERT_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    default:
      return state;
  }
};

export default messageReducer;
