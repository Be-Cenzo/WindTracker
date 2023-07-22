import '../css/bottombar.css';
import searchIcon from '../img/search.png';
import refreshIcon from '../img/refresh.png';


const Bottombar = (props) => {

    const searchBtn = <button onClick={props.refresh}>
                            <img className='icon' src={searchIcon.src}/>
                        </button>
    
    const refreshBtn = <button onClick={props.refresh}>
                            <img className='icon' src={refreshIcon.src}/>
                        </button>

    return(
        <div className='bottombar-container'>
            <div class="search-button bottombar-object">
                {searchBtn}
            </div>
            <div className="bottombar">
                <div>
                    <h1 className='text-center-mt-5'>WindTracker</h1>
                    <div className='bottombar-buttons-small'>
                        {searchBtn}
                        {refreshBtn}
                    </div>
                </div>
            </div>
            <div class="refresh-button bottombar-object">
                {refreshBtn}
            </div>
        </div>
    );
}

export default Bottombar;