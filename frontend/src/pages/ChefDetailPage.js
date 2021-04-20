import React from 'react';
import PageContainer from '../containers/PageContainer';
import Rating from '../components/Rating';
import TabBtn from '../components/TabBtn';
import classes from './ChefDetailPage.module.css';
import chef1 from '../images/chef1.jpg';
import food1 from '../images/food1.jpg';
import food2 from '../images/food2.jpg';
import food3 from '../images/food3.jpg';

const tabs = [{ text: 'description' }, { text: 'reviews' }];

const ChefDetailPage = () => {
  return (
    <PageContainer>
      <div className={classes.btnUpdateContainer}>
        <button className={classes.btnUpdate}>Update Page</button>
      </div>

      <div className={classes.contentContainer}>
        <img src={chef1} alt="Mike" className={classes.chefImage} />
        <h2 className={classes.name}>Mike</h2>
        <h4 className={classes.categories}>Western</h4>

        <div className={classes.ratingContainer}>
          <Rating />
        </div>

        <ul className={classes.tabsContainer}>
          {tabs.map((tab, index) => (
            <TabBtn key={index} {...tab} />
          ))}
        </ul>

        <div className={classes.foodImageContainer}>
          <img src={food1} alt="food1" className={classes.foodImage} />
          <img src={food2} alt="food2" className={classes.foodImage} />
          <img src={food3} alt="food3" className={classes.foodImage} />
        </div>

        <p className={classes.description}>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus
          posuere dui facilisis massa vehicula rutrum. Sed id malesuada orci.
          Duis ac dolor ultricies turpis consequat pulvinar. Nullam odio ante,
          semper sed nunc egestas, tincidunt venenatis libero. Curabitur semper
          sem vel augue hendrerit congue. Ut augue nunc, pharetra nec mattis at,
          consectetur sit amet nisl.
        </p>
      </div>
    </PageContainer>
  );
};

export default ChefDetailPage;
