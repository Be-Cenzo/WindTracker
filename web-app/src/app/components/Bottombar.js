import '../css/bottombar.css';
import searchIcon from '../img/search.png';
import refreshIcon from '../img/refresh.png';
import upArrow from '../img/up.png';
import downArrow from '../img/down.png';
import { useState } from 'react';


const Bottombar = (props) => {
    const searchBtn = <button onClick={props.refresh}>
                            <img className='icon' src={searchIcon.src}/>
                        </button>
    
    const refreshBtn = <button onClick={props.refresh}>
                            <img className='icon' src={refreshIcon.src}/>
                        </button>

    const open = <div className='bottombar-content'>
                    <div className='bottombar-toggle'>
                        <img className='icon' src={downArrow.src} onClick={(e) => props.setIsOpen(false)} />
                    </div>
                        {props.children}
                </div>
    
    const closed = <div className='bottombar-content'>
                        <div className='bottombar-toggle'>
                            <img className='icon' src={upArrow.src} onClick={(e) => props.setIsOpen(true)}/>
                        </div>
                    </div>

    return(
        <div className='bottombar-container'>
            <div className="bottombar">
                {props.isOpen ? open : closed}
            </div>
        </div>
    );
}

export default Bottombar;