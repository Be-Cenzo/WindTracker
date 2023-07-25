import '../css/navbar.css';
import searchIcon from '../img/search.png';
import refreshIcon from '../img/refresh.png';


const Navbar = (props) => {

    const searchBtn = <button  className='nav-button' onClick={props.openBottombar}>
                            <img className='icon' src={searchIcon.src}/>
                        </button>
    
    const refreshBtn = <button className='nav-button' onClick={props.refresh}>
                            <img className='icon' src={refreshIcon.src}/>
                        </button>

    return(
        <div className='navbar-container'>
            <div class="search-button navbar-object">
                {searchBtn}
            </div>
            <div className="navbar">
                <div>
                    <h1 className='text-center-mt-5'>WindTracker</h1>
                    <div className='navbar-buttons-small'>
                        {searchBtn}
                        {refreshBtn}
                    </div>
                </div>
            </div>
            <div class="refresh-button navbar-object">
                {refreshBtn}
            </div>
        </div>
    );
}

export default Navbar;