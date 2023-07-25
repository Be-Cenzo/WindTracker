import '../css/marker.css';
import icn from '../img/wind-turbine.png'

const MarkerCard = (props) => {
    const date = new Date(props.marker.lastUpdated*1000).toString();
    return(
        <div className="marker-card">
            <div className='marker-card-panel'>
                <img className='card-icon' src={icn.src}/>
            </div>
            <div className='marker-card-panel right-panel'>
                <div>
                    <strong>Name:</strong> {props.marker.sensorName}
                </div>
                <div>
                    <strong>Wind Speed:</strong> {props.marker.windSpeed}km/h
                </div>
                <div>
                    <strong>Wind Direction:</strong> {props.marker.windDirection}
                </div>
                <div>
                    <strong>Last Updated:</strong> {date}
                </div>
                <div>
                    <strong>Error:</strong> {props.marker.error.toString()}
                </div>
            </div>
        </div>
    );
}

export default MarkerCard;