import React from 'react';
import { Route, Switch } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import SearchPage from '../pages/SearchPage';
import ChefDetailPage from '../pages/ChefDetailPage';
import LoginPage from '../pages/LoginPage';
import SingleChatPage from '../pages/SingleChatPage';
import ChatsPage from '../pages/ChatsPage';
import Navbar from './Navbar';
import Header from './Header';
import SideBar from './SideBar';
import classes from './App.module.css';

function App() {
  return (
    <div className={classes.pageContainer}>
      <div className={classes.contentContainer}>
        <Navbar />
        <Header />
        <Switch>
          <Route path="/" exact component={HomePage} />
          <Route path="/login" component={LoginPage} />
          <Route path="/search/:term" component={SearchPage} />
          <Route path="/chefs/:id" component={ChefDetailPage} />
          <Route path="/chats/:receiverEmail" component={SingleChatPage} />
          <Route path="/chats" component={ChatsPage} />
        </Switch>
      </div>
      <div className={classes.sidebarContainer}>
        <SideBar />
      </div>
    </div>
  );
}

export default App;
