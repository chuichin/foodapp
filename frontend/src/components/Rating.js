import React from 'react';
import { FaStar, FaRegStar } from 'react-icons/fa';
import classes from './Rating.module.css';

const Rating = () => {
  return (
    <ul className={classes.list}>
      <li className={classes.item}>
        <FaStar className={classes.filled} />
      </li>
      <li className={classes.item}>
        <FaStar className={classes.filled} />
      </li>
      <li className={classes.item}>
        <FaStar className={classes.filled} />
      </li>
      <li className={classes.item}>
        <FaStar className={classes.filled} />
      </li>
      <li className={classes.item}>
        <FaRegStar className={classes.fill} />
      </li>
    </ul>
  );
};

export default Rating;
