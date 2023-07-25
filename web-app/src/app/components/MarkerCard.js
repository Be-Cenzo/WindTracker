import '../css/marker.css';

const MarkerCard = (props) => {
    const date = new Date(props.marker.lastUpdated*1000).toString();
    return(
        <div className="marker-card">
            Name: {props.marker.sensorName}<br/>Wind Speed: {props.marker.windSpeed}km/h<br/>Wind Direction: {props.marker.windDirection}<br/>Last Updated: {date}<br/>Error: {props.marker.error.toString()}
        </div>
    );
}

export default MarkerCard;