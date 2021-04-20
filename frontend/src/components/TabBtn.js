import React from 'react';
import classes from './TabBtn.module.css';

const TabBtn = ({ text }) => {
  return (
    <li className={classes.item}>
      <button className={classes.btnTab}>{text}</button>
    </li>
  );
};

export default TabBtn;
