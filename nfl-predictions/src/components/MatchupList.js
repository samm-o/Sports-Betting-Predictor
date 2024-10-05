import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Matchup from './Matchup';

const weekMatchupCounts = [16, 16, 16, 16, 14, 14, 15, 16, 15, 14, 14, 13, 16, 13, 16, 16, 16, 16];

const groupMatchupsByWeek = (matchups) => {
  const weeks = [];
  let startIndex = 0;

  weekMatchupCounts.forEach((count, weekIndex) => {
    const weekMatchups = matchups.slice(startIndex, startIndex + count);
    weeks.push({ week: weekIndex + 1, matchups: weekMatchups });
    startIndex += count;
  });

  return weeks;
};

const MatchupList = () => {
  const [weeks, setWeeks] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/matchups') // Replace with your backend endpoint
      .then(response => {
        console.log('Fetched data:', response.data); // Add this line
        const groupedMatchups = groupMatchupsByWeek(response.data);
        setWeeks(groupedMatchups);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="matchup-list">
      {weeks.map((week) => (
        <div key={week.week} className="week-section">
          <h2>Week {week.week}</h2>
          {week.matchups.map((matchup, index) => (
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
      ))}
    </div>
  );
};

export default MatchupList;