import React from 'react';
import {
  FaUtensils,
  FaGlassMartiniAlt,
  FaQuestionCircle,
  FaInfoCircle,
  FaHeadset,
  FaHome,
} from 'react-icons/fa';
import { connect } from 'react-redux';
import { motion } from 'framer-motion';
import { toggleNav } from '../actions';
import NavItem from './NavItem';
import classes from './Navbar.module.css';

const navItems = [
  { text: 'Home', icon: <FaHome />, path: '/' },
  { text: 'Sign Up', icon: <FaUtensils />, path: '/signup' },
  { text: 'Log In', icon: <FaGlassMartiniAlt />, path: '/login' },
  { text: 'About Us', icon: <FaInfoCircle />, path: '/aboutus' },
  { text: 'Support', icon: <FaHeadset />, path: '/support' },
  { text: 'FAQ', icon: <FaQuestionCircle />, path: '/faq' },
];

const backgroundVariant = {
  open: {
    scale: 200,
    transition: {
      duration: 1,
    },
  },
  close: {
    scale: 1,
    transition: {
      duration: 1,
    },
  },
};

const navListVariant = {
  open: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
  close: {
    transition: {
      staggerChildren: 0.1,
      staggerDirection: -1,
    },
  },
};

const navVariant = {
  open: {
    visibility: 'visible',
  },
  close: {
    visibility: 'hidden',
    transition: {
      delay: 1,
    },
  },
};

const Navbar = props => {
  return (
    <div className={classes.navigation}>
      <input
        type="checkbox"
        id="nav-toggle"
        className={classes.checkbox}
        onClick={props.toggleNav}
      />
      <label htmlFor="nav-toggle" className={classes.label}>
        <span className={`${classes.line}`}></span>
      </label>

      <motion.div
        animate={props.isNavOpen ? 'open' : 'close'}
        variants={backgroundVariant}
        className={classes.navBackground}
      >
        &nbsp;
      </motion.div>

      <motion.nav
        className={classes.nav}
        variants={navVariant}
        animate={props.isNavOpen ? 'open' : 'close'}
        initial="close"
      >
        <motion.ul className={classes.navList} variants={navListVariant}>
          {navItems.map((item, index) => (
            <NavItem key={index} {...item} />
          ))}
        </motion.ul>
      </motion.nav>
    </div>
  );
};

const mapStateToProps = state => {
  return {
    isNavOpen: state.ui.isNavOpen,
  };
};

export default connect(mapStateToProps, { toggleNav })(Navbar);
