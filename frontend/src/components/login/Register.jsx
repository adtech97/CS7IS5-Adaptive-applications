

import React from "react";
import loginImg from "../../login.svg";
import axios from "axios";
import { Navigate } from "react-router-dom";

export class Register extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      email: "",
      password: "",
      redirect: false
    };
  }

  handleInputChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  };

  handleRegister = () => {
    const fromData = new FormData();
    fromData.append("name", this.state.username);
    fromData.append("email", this.state.email);
    fromData.append("password", this.state.password);
    const { username, email, password } = this.state;
    axios.post("http://127.0.0.1:8080/signup/", fromData)
      .then(response => {
        if (response.data.message === "User created successfully") {
          this.setState({ redirect: true });
        }
      })
      .catch(error => {
        console.log(error);
      });
  };

  render() {
    if (this.state.redirect) {
      return <Navigate to="/login" />;
    }

    return (
      <div className="base-container" ref={this.props.containerRef}>
        <div className="header">Register</div>
        <div className="content">
          <div className="image">
            <img src={loginImg} />
          </div>
          <div className="form">
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                name="username"
                placeholder="username"
                value={this.state.username}
                onChange={this.handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="text"
                name="email"
                placeholder="email"
                value={this.state.email}
                onChange={this.handleInputChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="text"
                name="password"
                placeholder="password"
                value={this.state.password}
                onChange={this.handleInputChange}
              />
            </div>
          </div>
        </div>
        <div className="footer">
          <button type="button" className="btn" onClick={this.handleRegister}>
            Register
          </button>
        </div>
      </div>
    );
  }
}