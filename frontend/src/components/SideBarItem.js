import React from 'react';
import { Link } from 'react-router-dom';
import classes from './SideBarItem.module.css';

const SideBarItem = ({ path, icon, text }) => {
  return (
    <li className={classes.listItem}>
      <Link to={path} className={classes.link}>
        <span className={classes.icon}>{icon}</span>
        {text}
      </Link>
    </li>
  );
};

export default SideBarItem;
