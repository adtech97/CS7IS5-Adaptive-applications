

import React from "react";
import "./App.scss";
import { Login, Register } from "./components/login/index";
import UserInfo from "./components/userInfo/UserInfo";
import Workouts from "./components/userInfo/WorkoutList";  // Assuming correct import path
import Meals from "./components/userInfo/WorkoutList";        // Assuming correct import path and file name
import Profile from "./components/userInfo/UserProfile";   // Assuming correct import path

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogginActive: true,
      isAuthenticated: document.cookie.includes('authToken'),
      currentSection: 'userInfo' // default to showing user info upon login
    };
  }

  componentDidMount() {
    if (this.container) {
      this.rightSide.classList.add("right");
    }
  }

  componentDidUpdate(prevProps, prevState) {
    const isLoggedIn = document.cookie.includes('authToken');
    if (isLoggedIn !== prevState.isAuthenticated) {
      this.setState({ isAuthenticated: isLoggedIn });
    }
  }

  changeState = () => {
    const { isLogginActive } = this.state;
    if (isLogginActive) {
      this.rightSide.classList.remove("right");
      this.rightSide.classList.add("left");
    } else {
      this.rightSide.classList.remove("left");
      this.rightSide.classList.add("right");
    }
    this.setState(prevState => ({ isLogginActive: !prevState.isLogginActive }));
  }

  navigateToDetails = (section) => {
    this.setState({ currentSection: section });
  };

  renderContent = () => {
    const { currentSection } = this.state;
    switch (currentSection) {
      case 'workouts':
        return <Workouts />;
      case 'meals':
        return <Meals />;
      case 'profile':
        return <Profile />;
      default:
        return <UserInfo navigateToDetails={this.navigateToDetails} />;
    }
  };

  render() {
    const { isLogginActive, isAuthenticated } = this.state;

    if (!isAuthenticated) {
      return (
          <div className="App">
            <div className="login">
              <div className="container" ref={ref => (this.container = ref)}>
                {isLogginActive ? (
                    <Login onLogin={() => this.setState({ isAuthenticated: true })} containerRef={ref => (this.current = ref)} />
                ) : (
                    <Register containerRef={ref => (this.current = ref)} />
                )}
              </div>
              <RightSide
                  current={isLogginActive ? "Register" : "Login"}
                  currentActive={isLogginActive ? "login" : "register"}
                  containerRef={ref => (this.rightSide = ref)}
                  onClick={this.changeState}
              />
            </div>
          </div>
      );
    }

    return this.renderContent();  // This function call replaces the switch-case in the render method.
  }
}

const RightSide = props => {
  const { current, currentActive, containerRef, onClick } = props;
  return (
      <div
          className="right-side"
          ref={containerRef}
          onClick={onClick}
      >
        <div className="inner-container">
          <div className="text">{currentActive}</div>
        </div>
      </div>
  );
};

export default App;