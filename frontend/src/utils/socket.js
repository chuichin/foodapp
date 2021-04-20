import io from 'socket.io-client';

const endpoint = 'ws://localhost:8000';

const socket = io(endpoint);

export default socket;
