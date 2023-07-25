'use client'

const { Marker, Popup, Tooltip } = require("react-leaflet");

import L from 'leaflet';
import marker from '../img/wind-marker.png';
import '../css/marker.css';
import { useEffect, useRef, useState } from 'react';

const myIcon = new L.Icon({
    iconUrl: marker.src,
    iconSize: [54, 72],
    iconAnchor: [27, 72]
});



const MarkerPoint = (props) => {
    const ref = useRef(null);
    const date = new Date(props.marker.lastUpdated*1000).toString();
    const errorClass = props.marker.error ? 'error' : '';

    const divIcon = new L.DivIcon({
        className: 'my-div-icon',
            html: <div>
                    <img class="my-div-image" src={marker}/>
                    <span class="my-div-span">' + {props.marker.windSpeed} + 'km/h</span>
                </div>  
    })

    const open = (e) => {
        props.openBottombar(e, props.marker);
    }  

    return(
        <>
        <Marker
            eventHandlers={{ click: open }}
            key={props.marker.sensorName}
            icon={myIcon}
            position={[
                props.marker.latitude,
                props.marker.longitude,
            ]}>
                <Tooltip ref={ref} permanent={true} direction='bottom' opacity={1} offset={[0, -10]} className='tooltip remove'>
                    <div className={'tooltip ' + errorClass}>
                        {props.marker.windSpeed}km/h
                    </div>
                </Tooltip>
        </Marker>
        </>
    );
}



export default MarkerPoint