import React from 'react';
import SortableItem from './SortableItem';
import { SortableContainer } from 'react-sortable-hoc';

const SortableList = (props) => {
    return (
        <div className='text-center justify-center justify-items-center content-center items-center '>
            {props.items.map((value, index) => (
                <SortableItem key={`item-${index}`} index={index} value={value} />
            ))}
        </div>
    );
}

export default SortableContainer(SortableList);