import React from 'react';
import {SortableElement} from 'react-sortable-hoc';

const SortableItem = (props) => {
    return <div className='max-w-2xl h-fit text-center rtl bg-purple-200 m-2 p-2 rounded-xl'>{props.value[1]}</div>
}
export default SortableElement(SortableItem);