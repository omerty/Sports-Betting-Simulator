import React, { useEffect, useState } from 'react';
import './HomeScreen.css';
import 'boxicons/css/boxicons.min.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SettingScreen() {
  const token = localStorage.getItem('token');
  const [events, setEvents] = useState([]);
  const [userData, setUserData] = useState({ email: '', coins: 0 });
  const [password, setPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [activeLink, setActiveLink] = useState('/Profile');
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/login');
    } else {
      axios.get('/api/userCoins', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(response => {
        setUserData({ email: response.data.email, coins: response.data.coins });
      }).catch(error => {
        console.error('Error fetching user data:', error);
      });

      axios.get('http://localhost:5000/api/allBets', {
        headers: { Authorization: `Bearer ${token}` }
      }).then(response => {
        console.log('Fetched events:', response.data);
        setEvents(response.data);
      }).catch(error => {
        console.error('Error fetching sports data:', error);
      });
    }
  }, [token, navigate]);

  const handlePasswordChange = () => {
    if (newPassword !== confirmPassword) {
      alert('New password and confirmation password do not match');
      return;
    }

    axios.post('/api/changePassword', { password, newPassword }, {
      headers: { Authorization: `Bearer ${token}` }
    }).then(response => {
      alert('Password changed successfully');
    }).catch(error => {
      console.error('Error changing password:', error);
      alert('Failed to change password');
    });
  };

  return (
    <div className="HomeScreen">
      {/* Sidebar navigation */}
      <div className="nav" id="nav">
        <nav className="nav__content">
          <div className="nav__toggle" id="nav-toggle">
            <i className='bx bx-chevron-right'></i>
          </div>

          <a href="#" className="nav__logo">
            <i className='bx bxs-heart'></i>
            <span className="nav__logo-name">Sports</span>
          </a>

          <div className="nav__list">
            <a href="/Soccer" className={`nav__link ${activeLink === '/Soccer' ? 'active-link' : ''}`}>
              <i className='bx bx-football'></i>
              <span className="nav__name">Soccer</span>
            </a>

            <a href="/Football" className={`nav__link ${activeLink === '/Football' ? 'active-link' : ''}`}>
              <i className='bx bx-ball' ></i>
              <span className="nav__name">NFL</span>
            </a>

            <a href="/Hockey" className={`nav__link ${activeLink === '/Hockey' ? 'active-link' : ''}`}>
              <i className='bx bxs-circle'></i>
              <span className="nav__name">NHL</span>
            </a>

            <a href="/Cricket" className={`nav__link ${activeLink === '/Cricket' ? 'active-link' : ''}`}>
              <i className='bx bx-cricket-ball'></i>
              <span className="nav__name">Cricket</span>
            </a>

            <a href="/Setting" className={`nav__link ${activeLink === '/Profile' ? 'active-link' : ''}`}>
              <i className='bx bx-cog'></i>
              <span className="nav__name">Profile</span>
            </a>
          </div>
        </nav>
      </div>

      {/* Settings Content */}
      <div className="settings">
        <h2>Settings</h2>
        <div className="settings__section">
          <h3>Profile</h3>
          <p>Email: {userData.email}</p>
          <p>Coins: {userData.coins}</p>
        </div>

        <div className="settings__section">
        <h3>Open Bets</h3>
        {events && events.bets && events.bets.length > 0 ? (
            <ul>
            {events.bets.map((bet, index) => (
                <li key={index}>
                <span>Bet Amount: {bet.bet_amount}</span><br />
                <span>Bet Details: {bet.bet_details}</span><br />
                <span>Estimated Winnings: {bet.expected_winnings}</span>
              </li>
            ))}
            </ul>
        ) : (
            <p>No open bets found.</p>
        )}
        </div>

        <div className="settings__section">
          <h3>Change Password</h3>
          <input
            type="password"
            placeholder="Current Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="Confirm New Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <button onClick={handlePasswordChange}>Change Password</button>
        </div>
      </div>
    </div>
  );
}

export default SettingScreen;
