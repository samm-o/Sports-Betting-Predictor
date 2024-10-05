import React from 'react';
import './Matchup.css';

const Matchup = ({ home, visitor, rfScore, gbScore, logregScore }) => {
  return (
    <div className="matchup">
      <h2>{home} vs {visitor}</h2>
      <div className="scores">
        <p>Random Forest: {rfScore}%</p>
        <p>Gradient Boost: {gbScore}%</p>
        <p>Logarithmic Regression: {logregScore}%</p>
      </div>
    </div>
  );
};

export default Matchup;