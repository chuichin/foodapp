const initialState = {
  isNavOpen: false,
  isLoading: false,
  isEmojiPickerOpen: false,
  isError: false,
};

const uiReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'TOGGLE_NAV':
      return { ...state, isNavOpen: !state.isNavOpen };
    case 'START_LOADING':
      return { ...state, isLoading: true };
    case 'STOP_LOADING':
      return { ...state, isLoading: false };
    case 'TOGGLE_EMOJI_PICKER':
      return { ...state, isEmojiPickerOpen: !state.isEmojiPickerOpen };
    case 'SET_ERROR':
      return { ...state, isError: true };
    case 'HIDE_ERROR':
      return { ...state, isError: false };
    default:
      return state;
  }
};

export default uiReducer;
