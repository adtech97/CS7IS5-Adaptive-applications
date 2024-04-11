import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import mealIcon2 from './assets/food_icon.png'
import workoutIcon2 from './assets/workout_icon2.png'
import profileIcon2 from './assets/user_icon.png'
import WorkoutList from "./WorkoutList";
import UserProfile from "./UserProfile";

const DetailPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { section } = location.state || {};

    const navigateToDetails = (newSection) => {
        navigate('/details', { state: { section: newSection } });
    };

    return (
        <div className="container">
            <div className="workoutIcon"  onClick={() => navigateToDetails('workouts')}>
                <span>WORKOUTS</span>
                <img src={workoutIcon2} alt="Workouts" className="iconImage"/>
            </div>
            <div className="mealIcon" onClick={() => navigateToDetails('meals')}>
                <span>MEALS</span>
                <img src={mealIcon2} alt="Meals" className="iconImage"/>
            </div>
            <div className="UserIcon" onClick={() => navigateToDetails('profile')}>
                <span>PROFILE</span>
                <img src={profileIcon2} alt="User Profile" className="iconImage"/>
            </div>
            <div className="restArea">
                {/* Content based on 'section' */}
                {section === 'workouts' && <WorkoutList />}
                {section === 'meals' && <span>Meal Details</span>}
                {section === 'profile' && <UserProfile />}
            </div>
        </div>
    );
};

export default DetailPage;