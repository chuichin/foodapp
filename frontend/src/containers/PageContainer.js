import React from 'react';
import classes from './PageContainer.module.css';

const PageContainer = props => {
  return <div className={classes.pageContainer}>{props.children}</div>;
};

export default PageContainer;
