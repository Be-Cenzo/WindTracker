'use client'

import React, { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet'
//import '../node_modules/leaflet/dist/leaflet.css'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet';
import marker from '../img/marker.png';
import MarkerPoint from './MarkerPoint';
import Navbar from './Navbar';
import '../css/map.css'
import Bottombar from './Bottombar';
const myIcon = new L.Icon({
    iconUrl: marker.src,
    iconSize: [60, 55]
});

const OpenStreetMap = () => {
  const [map, setMap] = useState(null);
  const [center, setCenter] = useState({ lat: 40.853294, lng: 14.305573 });
  const [position, setPosition] = useState({loaded: true, error : false, coordinates: { lat: 40.853294, lng: 14.305573 }});
  const [markers, setMarkers] =  useState({loaded: true, error : false, markers: [{name: "Sensor0", latitude: 42.853294, longitude: 14.305573 }]});
  const [isPositioning, setIsPositioning] = useState(false);
  const ZOOM_LEVEL = 13
  const mapRef = useRef()
  const restId = "yxf0kstcl3"
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

  const pickAPosition = () => {
    /*console.log(mapRef);
    map.locate().on("locationfound", function (e) {
      setPosition(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
    });*/
    setIsPositioning(true);
  }

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

  const PositionHandler = () => {
    const map = useMapEvents({
        click: (e) => {
          if(isPositioning){
            let pos = {... position};
            pos.coordinates = e.latlng;
            console.log(e.latlng);
            setPosition(pos);
            setIsPositioning(false);
          }
        }
    });
    return null;
};

  return (
    <>
      <div className='container'>
        <Navbar refresh={refresh} position={pickAPosition}/>
        <div className='map-container'>
            <MapContainer center={center} zoom={ZOOM_LEVEL} ref={mapRef} className='map' whenReady={setMap}>
              <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
              />
              {markers.loaded && !markers.error && markers.markers.map(element => <MarkerPoint marker={element}/>)}

              {position.loaded && !position.error && (
                <Marker
                icon={myIcon}
                position={[
                    position.coordinates.lat,
                    position.coordinates.lng,
                ]}
                ></Marker>
              )}
              <PositionHandler />
            </MapContainer>
        </div>

        <Bottombar />
      </div>
    </>
  )
}

export default OpenStreetMap
