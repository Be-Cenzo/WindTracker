'use client'

const { Marker, Popup } = require("react-leaflet");

import L from 'leaflet';
import marker from '../img/wind.png';

const myIcon = new L.Icon({
    iconUrl: marker.src,
    iconSize: [60, 55]
});

const MarkerPoint = (props) => {
    const date = new Date(props.marker.lastUpdated*1000).toString();
    console.log(props);
    console.log("data");
    console.log(date);
    return(
        <Marker
            key={props.marker.name}
            icon={myIcon}
            position={[
                props.marker.latitude,
                props.marker.longitude,
            ]}>
                <Popup>
                    Name: {props.marker.name}<br/>Wind Speed: {props.marker.windSpeed}<br/>Wind Direction: {props.marker.windDirection}<br/>Last Updated: {date}
                </Popup>
        </Marker>
    );
}



export default MarkerPoint