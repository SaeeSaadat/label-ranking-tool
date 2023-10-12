import React from 'react';
import {SortableElement} from 'react-sortable-hoc';

const SortableItem = (props) => {
    return <div className='max-w-2xl h-fit text-center rtl bg-cyan-100 m-2 p-2 rounded-xl select-none flex flex-row justify-between'>
        <div className='min-h-full align-baseline justify-center flex flex-col align-middle'>
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-list"
                 viewBox="0 0 25 25">
                <path fillRule="evenodd"
                      d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"/>
            </svg>
        </div>
        <div className='text-right px-2'>
            {props.value[1]}
        </div>
    </div>
}
export default SortableElement(SortableItem);