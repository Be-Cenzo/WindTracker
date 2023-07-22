'use client'

const { Marker, Popup, Tooltip } = require("react-leaflet");

import L from 'leaflet';
import marker from '../img/wind.png';
import '../css/marker.css';

const myIcon = new L.Icon({
    iconUrl: marker.src,
    iconSize: [60, 55]
});



const MarkerPoint = (props) => {
    const date = new Date(props.marker.lastUpdated*1000).toString();
    console.log(props);
    console.log("data");
    console.log(date);

    const divIcon = new L.DivIcon({
        className: 'my-div-icon',
            html: <div>
                    <img class="my-div-image" src={marker}/>
                    <span class="my-div-span">' + {props.marker.windSpeed} + 'km/h</span>
                </div>  
    })

    return(
        <>
        <div id={props.marker.name}>
        </div>
        <Marker
            key={props.marker.name}
            icon={myIcon}
            position={[
                props.marker.latitude,
                props.marker.longitude,
            ]}>
                <Popup>
                    Name: {props.marker.name}<br/>Wind Speed: {props.marker.windSpeed}km/h<br/>Wind Direction: {props.marker.windDirection}<br/>Last Updated: {date}
                </Popup>
                <Tooltip permanent={true} direction='bottom' opacity={1} offset={[0, 20]} className='tooltip'>
                    {props.marker.windSpeed}km/h
                </Tooltip>
        </Marker>
        </>
    );
}



export default MarkerPoint