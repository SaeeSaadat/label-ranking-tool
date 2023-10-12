import React, {useEffect, useState} from 'react';
import Reorder, {
    reorder,
    reorderImmutable,
    reorderFromTo,
    reorderFromToImmutable
} from 'react-reorder';
import SortableList from "./SortableList";
import {arrayMoveImmutable} from "array-move";

const QuestionPage = (props) => {
        const [question, setQuestion] = useState({});
        const [items, setItems] = useState([]);
        const [error, setError] = useState('');
        const onSortEnd = ({oldIndex, newIndex}) => {
            setItems(prevItem => (arrayMoveImmutable(prevItem, oldIndex, newIndex)));
        };

        const handleNextClick = (event) => {
            event.preventDefault();
            fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json',},
                body: JSON.stringify({
                    "username": props.username,
                    "row_num": props.firstQuestion.row_num,
                    "informal": props.firstQuestion.informal,
                    "rankings": items.map(item => parseInt(item[0]))
                }),
            }).then((response) => {
                if (response.ok) {
                    props.handleQ();
                    return response.json();
                } else {
                    setError('error from server');
                }
            })
                .then((data) => {
                    // Handle successful response
                    // ...
                }).catch((error) => {
                setError(error.message);
            });
        }

        useEffect(() => {
            setQuestion(props.firstQuestion)
            setItems(
                Object.entries(props.firstQuestion.formals).map(([id, text]) => ([
                    id,
                    text
                ]))
            )
        }, [props.firstQuestion]);

        return (
            <div>
                <h2>جمله غیر رسمی</h2>
                <p>{question.informal}</p>
                <h2>لطفا جملات رسمی شده زیر را به ترتیبی به که نظر شما صحیح‌تر است مرتب کنید.</h2>
                <SortableList items={items} onSortEnd={onSortEnd}/>
                <div>شما تا کنون
                    در برچسب‌گذاری {question['user_answer_count']} داده مشارکت کرده‌اید.
                </div>
                <button onClick={handleNextClick}>ذخیره و جمله بعدی</button>
                <button>ذخیره و اتمام مشارکت</button>
                {error && <div style={{color: 'red'}}>{error}</div>}
            </div>
        );
    }
;

export default QuestionPage