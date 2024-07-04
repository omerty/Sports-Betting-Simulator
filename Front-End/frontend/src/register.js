
import React, { useState } from 'react';
import { useNavigate  } from 'react-router-dom';
import axios from 'axios';
import './styles.css';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();


  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/register', {
        email,
        password
      });
      setMessage(response.data.message);
      navigate('/');
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.error);
      } else {
        setMessage('An error occurred. Please try again.');
      }
    }
  };

  return (
    <div className="Register">
      <img src="loginbkg.png" alt="login image" className="login__img" />

      <form className="Register__form" onSubmit={handleSubmit}>
        <h1 className="Register__title">Register</h1>

        <div className="Register__content">
          <div className="Register__box">
            <i className="ri-user-3-line Register__icon"></i>

            <div className="Register__box-input">
              <input
                type="email"
                required
                className="Register__input"
                id="Register-email"
                placeholder=""
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <label htmlFor="Register-email" className="Register__label">Email</label>
            </div>
          </div>

          <div className="Register__box">
            <i className="ri-lock-2-line Register__icon"></i>

            <div className="Register__box-input">
              <input
                type="password"
                required
                className="Register__input"
                id="Register-pass"
                placeholder=" "
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <label htmlFor="Register-pass" className="Register__label">Password</label>
              <i className="ri-eye-off-line Register__eye" id="Register-eye"></i>
            </div>
          </div>
        </div>

        <div className="Register__check">
          <div className="Register__check-group">
            <input type="checkbox" className="Register__check-input" id="Register-check" />
            <label htmlFor="Register-check" className="Register__check-label">Remember me</label>
          </div>

        </div>

        <button type="submit" className="Register__button">Register</button>


        {message && <p className="Register__message">{message}</p>}
      </form>
    </div>
  );
}

export default Register;
