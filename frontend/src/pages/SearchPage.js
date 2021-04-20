import React from 'react';
import { FaSlidersH } from 'react-icons/fa';
import PageContainer from '../containers/PageContainer';
import SearchInput from '../components/SearchInput';
import ChefCard from '../components/ChefCard';
import classes from './SearchPage.module.css';

const SearchPage = props => {
  const { term } = props.match.params;

  return (
    <PageContainer>
      <h1 className={classes.heading}>{`Search for: ${term}`}</h1>

      <SearchInput />

      <ul className={classes.filterContainer}>
        <li className={classes.item}>
          <button className={classes.btnFilter}>
            <FaSlidersH />
          </button>
        </li>

        <li className={classes.item}>
          <select name="sort" id="sort" className={classes.btnSelect}>
            <option value="">Sort by</option>
            <option value="">Recommended</option>
            <option value="">Popularity</option>
            <option value="">Rating</option>
          </select>
        </li>

        <li className={classes.item}>
          <button className={classes.btnCategories}>Categories</button>
        </li>
      </ul>

      <ul className={classes.cardsContainer}>
        <ChefCard />
        <ChefCard />
        <ChefCard />
        <ChefCard />
      </ul>
    </PageContainer>
  );
};

export default SearchPage;
