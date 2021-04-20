import React from 'react';
import { Link } from 'react-router-dom';
import { FaFacebook, FaInstagram, FaTwitter } from 'react-icons/fa';
import Logo from './Logo';
import classes from './Footer.module.css';

const footerLinks = [
  { text: 'About Us', path: '/aboutus' },
  { text: 'Privacy', path: '/privacy' },
  { text: 'FAQ', path: '/faq' },
];

const socialLinks = [
  { icon: <FaFacebook />, path: 'https://www.facebook.com/' },
  { icon: <FaInstagram />, path: 'https://www.instagram.com' },
  { icon: <FaTwitter />, path: 'https://www.twitter.com' },
];

const Footer = () => {
  return (
    <footer className={classes.footer}>
      <Logo />

      <ul className={classes.linksList}>
        {footerLinks.map((link, index) => (
          <li key={index} className={classes.linksItem}>
            <Link to={link.path} className={classes.link}>
              {link.text}
            </Link>
          </li>
        ))}
      </ul>

      <ul className={classes.socialList}>
        {socialLinks.map((link, index) => (
          <li key={index} className={classes.socialItem}>
            <Link to={link.path} className={classes.socialLink}>
              {link.icon}
            </Link>
          </li>
        ))}
      </ul>
    </footer>
  );
};

export default Footer;
