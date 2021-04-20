import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import classes from './NavItem.module.css';

const item = {
  open: {
    opacity: 1,
    y: 0,
  },
  close: {
    opacity: 0,
    y: 50,
  },
};

const NavItem = ({ text, icon, path }) => {
  return (
    <motion.li
      className={classes.navItem}
      variants={item}
      whileHover={{ x: 10 }}
    >
      <Link to={path} className={classes.link}>
        <span className={classes.itemLogo}>{icon}</span>
        {text}
      </Link>
    </motion.li>
  );
};

export default NavItem;
