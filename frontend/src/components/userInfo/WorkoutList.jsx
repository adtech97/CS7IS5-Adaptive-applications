import React, { useState } from 'react';
import './WorkoutList.css'; // Ensure you have the CSS file with the required styles
import WorkoutPopup from "./WorkoutPopup";
import workoutIcon2 from './assets/workout_icon2.png'

// place holder for api call
const workouts = [
    { id: 1, name: 'BICEP CURL' , desc: 'this exercise is a bicep curl bla bla bla', bodyPart: 'arms', equip: 'dumbbell'},
    { id: 2, name: 'TREADMILL' , desc: 'this exercise is a treadmill bla bla bla', bodyPart: 'legs', equip: 'treadmill'},
    { id: 3, name: 'PLANKING', desc: 'this exercise is a treadmill bla bla bla', bodyPart: 'fullBody', equip: 'body only'},
];

const WorkoutList = () => {
    const [selectedWorkout, setSelectedWorkout] = useState(null);

    const getEquipmentImage = (equip) => {
        if (equip === 'body only') {
            return null;
        } else {
            return workoutIcon2;
        }
    };

    const handleClick = (workout) => {
        setSelectedWorkout(workout);
    };

    return (
        <div>
            <div className="workout-header">WORK OUT RECOMMENDATIONS</div>
            <div className="workout-list-container"> {/* Scrollable container */}
                {workouts.map((workout) => (
                    <div key={workout.id} className="workout-item" onClick={() => handleClick(workout)}>
                        <div>
                            <span className="workout-name">{workout.name}</span>
                            {/* Include additional information like description, bodyPart, etc. */}
                            {/*<span className="workout-description">{workout.desc}</span>*/}
                            {/*<span className="workout-equipment">{workout.equip}</span>*/}
                            {/*<span className="workout-bodypart">{workout.bodyPart}</span>*/}
                        </div>
                        { getEquipmentImage(workout.equip) && <img src={getEquipmentImage(workout.equip)} alt={workout.equip} className="workout-equip-img" /> }
                    </div>
                ))}
            </div>

            {/* Popup component */}
            {selectedWorkout && (
                <WorkoutPopup workout={selectedWorkout} onClose={() => setSelectedWorkout(null)} />
            )}
        </div>
    );
};

export default WorkoutList;
