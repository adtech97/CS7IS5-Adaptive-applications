
import React from "react";
import axios from "axios";
import loginImg from "../../login.svg";

export class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: ""
    };
  }

  handleInputChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  handleLogin = async () => {
    try {
      
      const fromData = new FormData();
      fromData.append("username", this.state.username);
      fromData.append("password", this.state.password);
      const response = await axios.post("http://127.0.0.1:8080/login/", fromData);
      const authToken = response.data.access_token;
      // Store the auth token in cookies here
      // Example: document.cookie = `authToken=${authToken}; path=/`;
      document.cookie = `authToken=${authToken}; path=/`;
    } catch (error) {
      console.error("Login failed", error);
    }
  }

  render() {
      return (
      <div className="base-container" ref={this.props.containerRef}>
        <div className="header">Login</div>
        <div className="content">
          <div className="image">
            <img src={loginImg} />
          </div>
          <div className="form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input type="text" name="username" placeholder="username" value={this.state.username} onChange={this.handleInputChange} />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="password" name="password" placeholder="password" value={this.state.password} onChange={this.handleInputChange} />
            </div>
          </div>
        </div>
        <div className="footer">
          <button type="button" className="btn" onClick={this.handleLogin}>
            Login
          </button>
        </div>
      </div>
    );
  }
}