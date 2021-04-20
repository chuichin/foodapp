import React from 'react';
import { FaChevronRight } from 'react-icons/fa';
import classes from './CategoriesBtn.module.css';

const CategoriesBtn = ({ category, icon }) => {
  return (
    <button className={classes.card}>
      <img src={icon} alt={category} className={classes.icon} />
      {category}
      <FaChevronRight className={classes.arrowIcon} />
    </button>
  );
};

export default CategoriesBtn;
