import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../images/logo.png';
import classes from './Logo.module.css';

const Logo = () => {
  return (
    <Link to="/">
      <img src={logo} alt="logo" className={classes.logo} />
    </Link>
  );
};

export default Logo;
