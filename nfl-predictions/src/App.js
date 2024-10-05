import React from 'react';
import MatchupList from './components/MatchupList';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>NFL 2024 Predictions</h1>
      </header>
      <MatchupList />
    </div>
  );
}

export default App;