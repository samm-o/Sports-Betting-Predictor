import React from 'react';
import './Matchup.css';

const Matchup = ({ home, visitor, rfScore, gbScore, logregScore }) => {
  return (
    <div className="matchup">
      <div className="matchup-header">
        <img src="/football.png" alt="Football Icon" className="football-icon left" />
        <h2>{home} vs {visitor}</h2>
        <img src="/football.png" alt="Football Icon" className="football-icon right" />
      </div>
      <div className="scores">
        <p>Random Forest: {rfScore}%</p>
        <p>Gradient Boost: {gbScore}%</p>
        <p>Logarithmic Regression: {logregScore}%</p>
      </div>
    </div>
  );
};

export default Matchup;