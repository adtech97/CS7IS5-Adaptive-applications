// import React from 'react';
// import { BrowserRouter as Router } from 'react-router-dom'; // Import Router
// import './Dashboard.css'
// import mealIcon2 from './assets/food_icon.png'
// import workoutIcon2 from './assets/workout_icon2.png'
// import profileIcon2 from './assets/user_icon.png'
// import { useNavigate } from 'react-router-dom';

// const UserInfo = () => {
//     const navigate = useNavigate();

//     const navigateToDetails = (section) => {
//         navigate('/details', { state: { section } });
//     };

//     return (
//         <Router> {/* Wrap with Router */}
//             <div className="container">
//                 <div className="workoutIcon"  onClick={() => navigateToDetails('workouts')}>
//                     <span>WORKOUTS</span>
//                     <img src={workoutIcon2} alt="Workouts" className="iconImage"/>
//                 </div>
//                 <div className="mealIcon" onClick={() => navigateToDetails('meals')}>
//                     <span>MEALS</span>
//                     <img src={mealIcon2} alt="Meals" className="iconImage"/>
//                 </div>
//                 <div className="UserIcon" onClick={() => navigateToDetails('profile')}>
//                     <span>PROFILE</span>
//                     <img src={profileIcon2} alt="User Profile" className="iconImage"/>
//                 </div>
//                 <div className="restArea">
//                     <span>Rest Area Content</span>
//                 </div>
//             </div>
//         </Router>
//     );
// };

// export default UserInfo;

import React from 'react';
import './Dashboard.css'
import mealIcon2 from './assets/food_icon.png'
import workoutIcon2 from './assets/workout_icon2.png'
import profileIcon2 from './assets/user_icon.png'


const UserInfo = ({ navigateToDetails }) => {
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
                <span>Rest Area Content</span>
            </div>
        </div>
    );
};

export default UserInfo;