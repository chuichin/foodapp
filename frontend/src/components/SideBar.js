import React from 'react';
import {
  FaUtensils,
  FaGlassMartiniAlt,
  FaQuestionCircle,
  FaInfoCircle,
  FaHeadset,
  FaHome,
} from 'react-icons/fa';
import logo from '../images/hamburger.png';
import SideBarItem from './SideBarItem';
import classes from './SideBar.module.css';

const navItems = [
  { text: 'Home', icon: <FaHome />, path: '/' },
  { text: 'Sign Up', icon: <FaUtensils />, path: '/signup' },
  { text: 'Log In', icon: <FaGlassMartiniAlt />, path: '/login' },
  { text: 'About Us', icon: <FaInfoCircle />, path: '/aboutus' },
  { text: 'Support', icon: <FaHeadset />, path: '/support' },
  { text: 'FAQ', icon: <FaQuestionCircle />, path: '/faq' },
];

const SideBar = () => {
  return (
    <div className={classes.sidebar}>
      <img src={logo} alt="hamburger" className={classes.logo} />
      <ul className={classes.list}>
        {navItems.map((item, index) => (
          <SideBarItem {...item} key={index} />
        ))}
      </ul>
    </div>
  );
};

export default SideBar;
