import React from 'react';
import { Link } from 'react-router-dom';
import classes from './OrangeBtn.module.css';

const OrangeBtn = ({ path, text }) => {
  return (
    <Link to={path} className={classes.btnOrange}>
      {text}
    </Link>
  );
};

export default OrangeBtn;
