import React, { useEffect, useState } from 'react';
import './UserProfile.css';

const UserProfile = () => {

    const [exercises, setExercises] = useState(['Exercise 1', 'Exercise 2', 'Exercise 3']); // Replace with actual data
    const [recipes, setRecipes] = useState(['Recipe 1', 'Recipe 2', 'Recipe 3']);

    // These are the initial settings
    const [focusAreas, setFocusAreas] = useState({
        arms: false,
        legs: false,
        back: false,
        chest: false,
        fullBody: false,
    });
    const [goals, setGoals] = useState({
        loseWeight: false,
        buildMuscle: false,
        increaseStamina: false,
    });
    const [allergies, setAllergies] = useState('');

    // Current simulated result from API call
    useEffect(() => {
        const fetchUserData = async () => {
            // Here we simulate fetching data with a delay
            const userData = await new Promise((resolve) => setTimeout(() => resolve({
                focusAreas: { arms: true, legs: true, back: false, chest: false, fullBody: true },
                goals: { loseWeight: true, buildMuscle: false, increaseStamina: true },
                allergies: 'Pollen, Dust',
            }), 1000)); // Delay of 1 second

            // Once the data is "fetched", update the states
            setFocusAreas(userData.focusAreas);
            setGoals(userData.goals);
            setAllergies(userData.allergies);
        };

        fetchUserData();
    }, []);

    // Handle change for checkboxes
    const handleFocusAreaChange = (event) => {
        setFocusAreas({ ...focusAreas, [event.target.name]: event.target.checked });
    };

    const handleGoalsChange = (event) => {
        setGoals({ ...goals, [event.target.name]: event.target.checked });
    };

    // Handle change for allergies input
    const handleAllergiesChange = (event) => {
        setAllergies(event.target.value);
    };

    // Handle form submission
    const handleSubmit = (event) => {
        event.preventDefault();
        // Process the data here or update the state
        console.log({ focusAreas, goals, allergies });
        // Implement saving changes...
    };

    // Function to clear all exercises from the list
    const clearExercises = () => {
        setExercises([]);
    };

    // Function to clear all recipes from the list
    const clearRecipes = () => {
        setRecipes([]);
    };

    return (
        <div className="user-profile-container">
            <div className="profile-column">
                <div className="scrollable-list user-info-list"> {/* Wrap the user info in a scrollable div */}
                    <form onSubmit={handleSubmit}>
                        <h2>Focus Areas</h2>
                        {Object.keys(focusAreas).map((area) => (
                            <div key={area}>
                                <input
                                    type="checkbox"
                                    id={area}
                                    name={area}
                                    checked={focusAreas[area]}
                                    onChange={handleFocusAreaChange}
                                />
                                <label htmlFor={area}>{area.charAt(0).toUpperCase() + area.slice(1)}</label>
                            </div>
                        ))}

                        <h2>Fitness Goals</h2>
                        {Object.keys(goals).map((goal) => (
                            <div key={goal}>
                                <input
                                    type="checkbox"
                                    id={goal}
                                    name={goal}
                                    checked={goals[goal]}
                                    onChange={handleGoalsChange}
                                />
                                <label htmlFor={goal}>{goal.replace(/([A-Z])/g, ' $1').trim().charAt(0).toUpperCase() + goal.replace(/([A-Z])/g, ' $1').trim().slice(1)}</label>
                            </div>
                        ))}

                        <h2>Allergies</h2>
                        <input
                            type="text"
                            value={allergies}
                            onChange={handleAllergiesChange}
                            placeholder="Enter your allergies"
                        />


                    </form>
                </div>
                <button type="submit">Save Changes</button>
            </div>

            <div className="history-column">
                <div className="scrollable-list exercises-list">
                    <h2>Exercise History</h2>
                    {exercises.map((exercise, index) => (
                        <div key={index} className="list-item">{exercise}</div>
                    ))}
                    <button onClick={clearExercises} className="clear-history-btn">Clear Exercise History</button>
                </div>

                <div className="scrollable-list recipes-list">
                    <h2>Recipe History</h2>
                    {recipes.map((recipe, index) => (
                        <div key={index} className="list-item">{recipe}</div>
                    ))}
                    <button onClick={clearRecipes} className="clear-history-btn">Clear Recipe History</button>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;

