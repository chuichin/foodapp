import React from 'react';
import { Link } from 'react-router-dom';
import Rating from './Rating';
import Heart from './Heart';
import chef1 from '../images/chef1.jpg';
import classes from './ChefCard.module.css';

const ChefCard = () => {
  return (
    <li className={classes.item}>
      <Link to="/chefs/12" className={classes.cardContainer}>
        <div className={classes.imageContainer}>
          <img src={chef1} alt="Mike" className={classes.chefImage} />
        </div>
        <div className={classes.detailContainer}>
          <p className={classes.name}>Mike</p>
          <p className={classes.category}>Western</p>
          <Rating />
          <p className={classes.price}>From RM 300</p>
        </div>
        <div className={classes.heartContainer}>
          <Heart />
        </div>
      </Link>
    </li>
  );
};

export default ChefCard;
