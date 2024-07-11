import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Welcome from './Welcome';
import FootBallScreen from './FootBall';
import Register from './register';
import SoccerScreen from './Main';
import CricketScreen from "./Cricket"
import HockeyScreen from "./Hockey"
import SettingScreen from './Settings';
import { AuthProvider } from './Authentication';
import './styles.css';

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Welcome />} />
        <Route path="/register" element={<Register />} />
        <Route path="/Soccer" element={<SoccerScreen />} />
        <Route path="/FootBall" element={<FootBallScreen/>} />
        <Route path="/Cricket" element={<CricketScreen/>} />
        <Route path="/Hockey" element={<HockeyScreen/>} />
        <Route path="/Setting" element={<SettingScreen/>} />
      </Routes>
    </AuthProvider>
  );
}

export default App;

