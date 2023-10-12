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
                ])).sort(() => Math.random() - 0.5)
        )
        }, [props.firstQuestion]);

        return (
            <section>
                <div
                    className="mx-auto max-w-screen-xl px-4 py-8 sm:py-12 sm:px-6 lg:py-16 lg:px-8"
                >
                    <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-16">
                        <div
                            className="relative h-64 overflow-hidden rounded-lg sm:h-80 lg:order-last lg:h-full"
                        >
                            {error && <div style={{color: 'red'}}>{error}</div>}
                            <SortableList items={items} onSortEnd={onSortEnd}/>
                        </div>

                        <div className="lg:py-24">
                            <h2 className="text-2xl font-bold sm:text-2xl">سوال {question['user_answer_count']}</h2>
                            <h3 className="text-xl sm:text-xl">لطفا جملات رسمی شده زیر را به ترتیبی به که نظر شما صحیح‌تر
                                است مرتب کنید.</h3>
                            <p className="mt-4 text-gray-600 text-xl">
                                <span className="text-lg font-bold sm:text-lg"> جمله غیر رسمی: </span>{question.informal}
                            </p>

                            <a
                                onClick={handleNextClick}
                                className="m-2 inline-block rounded border border-indigo-600 bg-indigo-600 px-12 py-3 text-sm font-medium text-white hover:bg-transparent hover:text-indigo-600 focus:outline-none focus:ring active:text-indigo-500"
                            >
                                ذخیره و جمله بعدی
                            </a>
                            <a
                                className="m-2 inline-block rounded border border-indigo-600 px-12 py-3 text-sm font-medium text-indigo-600 hover:bg-indigo-600 hover:text-white focus:outline-none focus:ring active:bg-indigo-500"
                            >
                                ذخیره و اتمام مشارکت
                            </a>
                        </div>
                    </div>
                </div>
            </section>
        );
    }
;

export default QuestionPage