// src/Welcome.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './Authentication';
import './styles.css';

function Welcome() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting login form');
    try {
      const response = await axios.post('http://localhost:5000/login', {
        email,
        password,
      });
      console.log('Login successful:', response.data.token);
      localStorage.setItem('token', response.data.token);
      login(response.data.token, response.data.username);
      setMessage(response.data.message);
      navigate('/Soccer');
    } catch (error) {
      console.error('Login error:', error); 
      if (error.response) {
        setMessage(error.response.data.error);
      } else {
        setMessage('An error occurred. Please try again.');
      }
    }
  };

  return (
    <div className="login">
      <img src="loginbkg.png" alt="login image" className="login__img" />

      <form className="login__form" onSubmit={handleSubmit}>
        <h1 className="login__title">Login</h1>

        <div className="login__content">
          <div className="login__box">
            <i className="ri-user-3-line login__icon"></i>

            <div className="login__box-input">
              <input
                type="email"
                required
                className="login__input"
                id="login-email"
                placeholder=""
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <label htmlFor="login-email" className="login__label">Email</label>
            </div>
          </div>

          <div className="login__box">
            <i className="ri-lock-2-line login__icon"></i>

            <div className="login__box-input">
              <input
                type="password"
                required
                className="login__input"
                id="login-pass"
                placeholder=" "
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <label htmlFor="login-pass" className="login__label">Password</label>
              <i className="ri-eye-off-line login__eye" id="login-eye"></i>
            </div>
          </div>
        </div>

        <div className="login__check">
          <div className="login__check-group">
            <input type="checkbox" className="login__check-input" id="login-check" />
            <label htmlFor="login-check" className="login__check-label">Remember me</label>
          </div>

          <a href="#" className="login__forgot">Forgot Password?</a>
        </div>

        <button type="submit" className="login__button">Login</button>

        <p className="login__register">
          Don't have an account? <a href="/Register">Register</a>
        </p>

        {message && <p className="login__message">{message}</p>}
      </form>
    </div>
  );
}

export default Welcome;
