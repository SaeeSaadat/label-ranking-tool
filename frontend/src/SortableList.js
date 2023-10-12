import React from 'react';
import SortableItem from './SortableItem';
import { SortableContainer } from 'react-sortable-hoc';

const SortableList = (props) => {
    return (
        <div className='border-amber-600'>
            {props.items.map((value, index) => (
                <SortableItem key={`item-${index}`} index={index} value={value} />
            ))}
        </div>
    );
}

export default SortableContainer(SortableList);