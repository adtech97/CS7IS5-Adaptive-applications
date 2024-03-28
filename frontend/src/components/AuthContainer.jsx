import React, { Component } from 'react';
import Login from './Login';
import Signup from './Signup';
import '../style.css'
class AuthContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showSignup: false,
    };
  }

  toggleSignup = () => {
    this.setState((prevState) => ({
      showSignup: !prevState.showSignup,
    }));
  };

  render() {
    const { showSignup } = this.state;
    return (
      <div className="auth-container">
        <div className="form-container">
          <Login />
        </div>
        {showSignup && (
          <div className="form-container">
            <Signup />
          </div>
        )}
        <button onClick={this.toggleSignup}>
          {showSignup ? 'Go to Login' : 'Sign Up'}
        </button>
      </div>
    );
  }
}

export default AuthContainer;