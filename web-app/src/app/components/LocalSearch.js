'use client'

import { useState } from 'react';
import '../css/localsearch.css';

const LocalSearch = (props) => {
    const [value, setValue] = useState(50);
    console.log("kitammuort")
    console.log(props)

    const startSearching = () => {
        console.log("Setto il searching")
        props.setIsSearching(true);
        props.search(value, props.markers);
    }

    return(
        <div className="localsearch-container">
            <h4>Live Updates On Sensors</h4>
            <div className="localsearch-position">
                Choose a position on the map
                <button onClick={() => props.position()}>Pick</button>
            </div>
            <div class="slider-container">
                Select the circle radius:
                <input type="range" min="1" max="100" value={value} class="slider" onInput={(e) => {setValue(e.target.value)}} />
                {value}
            </div>
            <button onClick={() => {startSearching()}}>Get Live Data</button>
            <button onClick={() => {props.setIsSearching(null) }}>Stop Live Data</button>
        </div>
    );
}

export default LocalSearch;