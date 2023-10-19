import React, {useEffect, useState} from 'react';
import SortableList from "./SortableList";
import {arrayMoveImmutable} from "array-move";


const QuestionPage = (props) => {
        const [question, setQuestion] = useState({});
        const [items, setItems] = useState([]);
        const [error, setError] = useState('');
        const [isLoading, setIsLoading] = useState(false);
        const onSortEnd = ({oldIndex, newIndex}) => {
            setItems(prevItem => (arrayMoveImmutable(prevItem, oldIndex, newIndex)));
        };

        const handleNextClick = (event, nextQ) => {
            setIsLoading(true);
            event.preventDefault();
            fetch(`${process.env.REACT_APP_API_HOST}/submit`, {
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
                    if (nextQ)
                        props.handleQ(true);
                    else
                        props.handleQ(false);
                    return response.json();
                } else {
                    try {
                        setError(response['detail']['msg']);
                    } catch (e) {
                        setError('خطایی پیش آمده است.')
                    }
                }
            })
                .then((data) => {
                    setIsLoading(false);
                }).catch((error) => {
                setError(error.message);
            });
        }

        useEffect(() => {
            setQuestion(props.firstQuestion)

            const sortmap = props.firstQuestion.previous_answer;
            let arr = Object.entries(props.firstQuestion.formals).map(([id, text]) => ([id, text]))

            arr.sort((a, b) => {
                const idA = parseInt(a[0]);
                const idB = parseInt(b[0]);
                const indexA = sortmap.indexOf(idA);
                const indexB = sortmap.indexOf(idB);
                if (idA === 7) {
                    return 1;
                }
                return indexA - indexB;
            });

            setItems(arr)
            // setItems(
            //     Object.entries(props.firstQuestion.formals).map(([id, text]) => ([
            //         id,
            //         text
            //     ])).sort(() => Math.random() - 0.5)
            // )
        }, [props.firstQuestion]);

        return (
            <section>
                <div
                    className="mx-auto max-w-screen-xl px-4 py-8 sm:py-12 sm:px-6 lg:py-16 lg:px-8"
                >
                    <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-16">
                        <div
                            className="relative h-64 overflow-scroll rounded-lg sm:h-80 lg:order-last lg:h-full"
                        >
                            {error && <div className='rounded-xl bg-red-100 text-red-800 p-2 m-2'>{error}</div>}
                            <SortableList items={items} onSortEnd={onSortEnd}/>
                        </div>

                        <div className="lg:py-24">
                            <h2 className="text-2xl font-bold">جمله شماره {question['row_num']}</h2>
                            <h3 className="text-sm">لطفا جملات رسمی شده زیر را به ترتیبی به که نظر شما صحیح‌تر
                                است مرتب کنید.</h3>
                            <p className="max-w-2xl h-fit text-center rtl bg-blue-100 m-2 p-2 rounded-xl select-none">
                                <span className="text-lg font-bold sm:text-lg"> جمله غیر رسمی: </span>{question.informal}
                            </p>

                            {isLoading ?
                                <a
                                    className="disabled m-2 inline-block rounded border border-indigo-600
                                     bg-indigo-100 px-12 py-3 text-sm font-medium text-white hover:bg-transparent
                                      hover:text-indigo-600 focus:outline-none focus:ring active:text-indigo-500"
                                >
                                    در حال پردازش
                                </a>
                                :
                                <a
                                    onClick={(event) => handleNextClick(event, true)}
                                    className="m-2 inline-block rounded border border-indigo-600 bg-indigo-600 px-12 py-3 text-sm font-medium text-white hover:bg-transparent hover:text-indigo-600 focus:outline-none focus:ring active:text-indigo-500"
                                >
                                    ذخیره و جمله بعدی
                                </a>
                            }

                            <a
                                onClick={(event) => handleNextClick(event, false)}
                                className="m-2 inline-block rounded border border-indigo-600 px-12 py-3 text-sm font-medium text-indigo-600 hover:bg-indigo-600 hover:text-white focus:outline-none focus:ring active:bg-indigo-500"
                            >
                                ذخیره و اتمام مشارکت
                            </a>
                            <h3 className="text-sm">
                                شما تا کنون در بررسی {question['user_answer_count']} جمله مشارکت کرده‌اید.
                            </h3>
                        </div>
                    </div>
                </div>
            </section>
        );
    }
;

export default QuestionPage