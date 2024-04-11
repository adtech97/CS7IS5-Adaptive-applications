import React from 'react';
import './WorkoutPopup.css'; // Make sure to create a corresponding CSS file
import workoutIcon2 from './assets/workout_icon2.png'
import personIcon from './assets/person_icon.png'
import backImage from './assets/back_icon.png'

const WorkoutPopup = ({ workout, onClose }) => {
    // Handle the completion of the workout
    const handleComplete = () => {
        // You might want to do something here, like updating a database or state
        onClose(); // Close the popup after marking as complete
    };

    const backButtonStyle = {
        display: 'inline-block', // or 'flex' if you need other flex properties
        width: '30px', // Width of your icon
        height: '30px', // Height of your icon
        border: 'none', // Removes the border
        background: 'transparent', // Makes the button transparent
        backgroundImage: `url(${backImage})`, // Path to your icon image
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
        backgroundSize: 'contain', // Ensures the icon fits within the button
        cursor: 'pointer',
    };

    return (
        <div className="workout-popup">
            <div className="workout-popup-content">
                <div className="workout-popup-header">
                    <button style={backButtonStyle} onClick={onClose} />
                    <div className="workout-info">
                        <div className="workout-equipment">
                            <img src={workoutIcon2} alt="Workouts" className="iconImage"/>
                            <span className="workout-text">{workout.equip}</span>
                        </div>
                        <div className="workout-bodypart-container">
                            <img src={personIcon} alt="Person" className="iconImage"/>
                            <span className="workout-text">{workout.bodyPart}</span>
                        </div>
                    </div>
                </div>
                <h2 className="workout-title">{workout.name}</h2>
                <p className="workout-description">{workout.desc}</p>
                <button className="complete-button" onClick={handleComplete}>EXERCISE COMPLETED</button>
            </div>
        </div>
    );
};

export default WorkoutPopup;