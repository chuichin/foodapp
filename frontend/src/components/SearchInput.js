import React from 'react';
import { FaSearch } from 'react-icons/fa';
import classes from './SearchInput.module.css';

const SearchInput = () => {
  return (
    <form className={classes.searchContainer}>
      <input
        type="text"
        className={classes.inputField}
        placeholder="Search chefs using categories"
      />
      <FaSearch className={classes.searchIcon} />
    </form>
  );
};

export default SearchInput;
