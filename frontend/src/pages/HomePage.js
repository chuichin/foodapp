import React from 'react';
import BtnViewMore from '../components/BtnViewMore';
import SearchInput from '../components/SearchInput';
import OrangeBtn from '../components/OrangeBtn';
import PageContainer from '../containers/PageContainer';
import CategoriesBtn from '../components/CategoriesBtn';
import ChefCard from '../components/ChefCard';
import hero from '../images/hero.png';
import classes from './HomePage.module.css';
import sliderData from '../utils/testdata/sliderData';

const HomePage = () => {
  return (
    <PageContainer>
      <section className={classes.hero}>
        <img src={hero} alt="hero" className={classes.heroImage} />
        <div>
          <h1 className={classes.heading}>
            Let the professionals do the work for you
          </h1>
          <OrangeBtn path="/learnmore" text="Learn More" />
        </div>
      </section>

      <section className={classes.categories}>
        <div className={classes.header}>
          <h2 className={classes.categoriesHeading}>Categories</h2>
          <BtnViewMore path="/categories" />
        </div>

        <SearchInput />

        <div className={classes.cardContainer}>
          {sliderData.map((data, index) => (
            <CategoriesBtn key={index} {...data} />
          ))}
        </div>
      </section>

      <section className={classes.contentSection}>
        <h2 className={classes.contentHeading}>Recommended</h2>

        <ul className={classes.chefCardContainer}>
          <ChefCard />
          <ChefCard />
          <ChefCard />
          <ChefCard />
        </ul>
      </section>
    </PageContainer>
  );
};

export default HomePage;
