'use client'

import React, { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker } from 'react-leaflet'
//import '../node_modules/leaflet/dist/leaflet.css'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet';
import marker from '../img/marker.png';
import MarkerPoint from './MarkerPoint';
const myIcon = new L.Icon({
    iconUrl: marker.src,
    iconSize: [60, 55]
});

const OpenStreetMap = () => {
  const [center, setCenter] = useState({ lat: 40.853294, lng: 14.305573 })
  const [location, setLocation] = useState({loaded: true, error : false, coordinates: { lat: 40.853294, lng: 14.305573 }})
  const [markers, setMarkers] =  useState({loaded: true, error : false, markers: [{name: "Sensor0", latitude: 42.853294, longitude: 14.305573 }]})
  const ZOOM_LEVEL = 13
  const mapRef = useRef()
  const restId = "b037v1j24d"
  const basePath = "http://localhost:4566/restapis/" + restId + "/local/_user_request_/";
  
  const updateMarkers = (points) => {
    setMarkers(points);
  }

  useEffect(() => {
    fetch(basePath + "getSensors")
    .then(result => result.json())
    .then(json => {
      let points = {loaded: true, error : false, markers: json.sensors};
      setMarkers(points);
      console.log(points);

      console.log(json.sensors[0].latitude);
      let point = {loaded: true, error : false, coordinates: { lat: json.sensors[2].latitude, lng: json.sensors[2].longitude }};
      console.log(point);
      return points;
    }).then(res => {
      let points = {...res}
      fetch(basePath + "getDataForSensor")
      .then(result => result.json())
      .then(json => {
        console.log(json);
        for(let i = 0; i < json.sensors.length; i++)
          for(let j = 0; j < points.markers.length; j++)
            if(json.sensors[i].name == points.markers[j].name){
              points.markers[j].windSpeed = json.sensors[i].windSpeed;
              points.markers[j].windDirection = json.sensors[i].windDirection;
              points.markers[j].lastUpdated = json.sensors[i].lastUpdated;
            }
        console.log(points);
        updateMarkers(points);
      });
    })
  }, []);

  useEffect(() => {
    console.log(markers);
    console.log("Salvato");
    //for(let i=0; i<markers.markers.length; i++){
      //console.log(markers.markers[i].name);
      
    //}
  }, [markers]);

  const refresh = () => {
    let points = {...markers};
    fetch(basePath + "getDataForSensor")
      .then(result => result.json())
      .then(json => {
        console.log(json);
        for(let i = 0; i < json.sensors.length; i++)
          for(let j = 0; j < points.markers.length; j++)
            if(json.sensors[i].name == points.markers[j].name){
              points.markers[j].windSpeed = json.sensors[i].windSpeed;
              points.markers[j].windDirection = json.sensors[i].windDirection;
              points.markers[j].lastUpdated = json.sensors[i].lastUpdated;
            }
        console.log(points);
        return points;
      })
      .then(points => setMarkers(points));
  }

  const print = () => {
    console.log(markers);
  }

  return (
    <>
      <div className='container'>
        <div className='container'>
          <h1 className='text-center-mt-5'>WindTracker</h1>
          <button onClick={refresh}>Refresh</button>
          <button onClick={print}>Stampa</button>
        </div>
        <div className='container' style={{height:"800vh", width:"100vw"}}>
            <MapContainer center={center} zoom={ZOOM_LEVEL} ref={mapRef}  style={{ height:"80vh",marginTop:"80px", marginBottom:'90px'
            }} >
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
            />
            {markers.loaded && !markers.error && markers.markers.map(element => <MarkerPoint marker={element}/>)}

            {location.loaded && !location.error && (
                <Marker
                icon={myIcon}
                position={[
                    location.coordinates.lat,
                    location.coordinates.lng,
                ]}
                ></Marker>
            )}
            </MapContainer>
        </div>

      </div>
    </>
  )
}

export default OpenStreetMap
