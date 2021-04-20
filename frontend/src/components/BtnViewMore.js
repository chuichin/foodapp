import React from 'react';
import { Link } from 'react-router-dom';
import { FaChevronRight } from 'react-icons/fa';
import classes from './BtnViewMore.module.css';

const BtnViewMore = ({ path }) => {
  return (
    <Link to={path} className={classes.btnViewMore}>
      View all
      <FaChevronRight className={classes.arrowIcon} />
    </Link>
  );
};

export default BtnViewMore;
