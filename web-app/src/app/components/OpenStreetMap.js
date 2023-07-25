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
import LocalSearch from './LocalSearch';
import MarkerCard from './MarkerCard';
import api from '../rest.json';
const myIcon = new L.Icon({
    iconUrl: marker.src,
    iconSize: [60, 55]
});

const OpenStreetMap = () => {

  console.log(api);
  const ZOOM_LEVEL = 13
  const mapRef = useRef()
  const restId = api.rest_api_id
  const basePath = "http://localhost:4566/restapis/" + restId + "/local/_user_request_/";

  const [center, setCenter] = useState({ lat: 40.853294, lng: 14.305573 });
  const [position, setPosition] = useState({loaded: true, error : false, coordinates: { lat: 40.853294, lng: 14.305573 }});
  const [markers, setMarkers] =  useState({loaded: false, error : false, markers: []});
  const [isOpen, setIsOpen] = useState(false);
  const [isPositioning, setIsPositioning] = useState(false);
  const [searchingInterval, setSearchingInterval] = useState(null);
  const [bottomBarPanel, setBottomBarPanel] = useState({component:"localSearch"});

  const pickAPosition = () => {
    /*console.log(mapRef);
    map.locate().on("locationfound", function (e) {
      setPosition(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
    });*/
    setIsPositioning(true);
  }

  const setSearch = (val) => {
    if(val == null)
      clearInterval(searchingInterval);
    setSearchingInterval(val);
  }

  const search = async (value, old) => {
    let positionPoint = new L.LatLng(position.coordinates.lat, position.coordinates.lng);
    console.log(positionPoint);
    
    let points = [];
    console.log(old);
    for(let i = 0; i<markers.markers.length; i++){
      let curr = new L.LatLng(markers.markers[i].latitude, markers.markers[i].longitude);
      if(positionPoint.distanceTo(curr, true)/1000 <= value)
        points.push(markers.markers[i]);
    }
    console.log("Invio i points");
    points = {sensors: points};
    console.log(JSON.stringify(points));
    console.log(searchingInterval);
    setSearchingInterval(setInterval(()=> localSearchCall(points), 2000));
  }

  const localSearchCall = (points) => {
      fetch(basePath + "localSearch", {
        method: "post",
        body: JSON.stringify(points)
      })
      .then(result => result.json())
      .then(json => {
        let points = {loaded: true, error : false, markers: json.sensors};
        setMarkers(points);
        console.log(points);
        return points;
      });
  }


  useEffect(() => {
    refresh();
  }, []);

  useEffect(() => {
    console.log("Is Searching?");
    console.log(searchingInterval);
  }, [searchingInterval]);

  useEffect(() => {
    console.log(markers);
    console.log("Salvato");
    //for(let i=0; i<markers.markers.length; i++){
      //console.log(markers.markers[i].name);
      
    //}
  }, [markers]);

  const refresh = () => {
    clearInterval(searchingInterval);
    setSearchingInterval(null);
    fetch(basePath + "getDataForSensor")
    .then(result => result.json())
    .then(json => {
      let points = {loaded: true, error : false, markers: json.sensors};
      setMarkers(points);
      console.log(points);
      return points;
    });
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
          else{
            setIsOpen(false);
          }
        }
    });
    return null;
};

  const openMarkerBottombar = (event, marker) => {
    console.log("Ciao " + marker.sensorName);
    const pos = markers.markers.indexOf(marker);
    setBottomBarPanel({component:"markerCard", marker:pos});
    setIsOpen(true);
  }

  const openSearchBottombar = (event) => {
    setBottomBarPanel({component:"localSearch"});
    setIsOpen(true);
  }

  return (
    <>
      <div className='container'>
        <Navbar refresh={refresh} openBottombar={openSearchBottombar}/>
        <div className='map-container'>
            <MapContainer center={center} zoom={ZOOM_LEVEL} ref={mapRef} className='map' >
              <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
              />
              {markers.loaded && !markers.error && markers.markers.map(element => <MarkerPoint marker={element} openBottombar={openMarkerBottombar}/>)}

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

        <Bottombar isOpen={isOpen} setIsOpen={setIsOpen}>
          {bottomBarPanel.component == "localSearch" ? <LocalSearch position={pickAPosition} search={search} markers={markers.markers} setIsSearching={setSearch}/> : <MarkerCard marker={markers.markers[bottomBarPanel.marker]} markers={markers.markers}/>}
        </Bottombar>
      </div>
    </>
  )
}

export default OpenStreetMap
