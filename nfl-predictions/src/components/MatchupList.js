import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Matchup from './Matchup';

const MatchupList = () => {
  const [matchups, setMatchups] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/matchups') // Replace with your backend endpoint
      .then(response => {
        console.log('Fetched data:', response.data); // Add this line
        setMatchups(response.data);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="matchup-list">
      {matchups.map((matchup, index) => (
        <Matchup
          key={index}
          home={matchup.Home}
          visitor={matchup.Visitor}
          rfScore={matchup.RF_HomeWinProbability}
          gbScore={matchup.GB_HomeWinProbability}
          logregScore={matchup.LogReg_HomeWinProbability}
        />
      ))}
    </div>
  );
};

export default MatchupList;