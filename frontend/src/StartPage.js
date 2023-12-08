import React, {useCallback, useEffect, useRef, useState} from 'react';
import QuestionPage from "./QuestionPage";
import ThanksPage from "./ThanksPage";
import {Tooltip as ReactTooltip} from 'react-tooltip'

const StartPage = () => {
    const username = useRef('');
    const [fiValue, setFiValue] = useState(null);
    const [isQuestion, setIsQuestion] = useState(false)
    const [isThanks, setIsThanks] = useState(false)
    const [firstQuestion, setFirstQuestion] = useState()
    const [questionPage, setQuestionPage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');


    const fetchFirstQuestion = useCallback(async () => {
        try {
            setIsLoading(true);
            let response
            if (fiValue) {
                response = await fetch(`${process.env.REACT_APP_API_HOST}/question_edit/` + fiValue);
            } else {
                setFiValue(username.current.value)
                response = await fetch(`${process.env.REACT_APP_API_HOST}/question_edit/` + username.current.value);
            }
            const jsonData = await response.json();
            if (response.ok)
                setFirstQuestion(jsonData);
            else if (response.status === 404) {
                console.log(response)
                if (jsonData.detail === "User not found")
                    setError('کاربری با این نام کاربری وجود ندارد.')
                else if (jsonData.detail === "No more questions left for you. Thanks for you contribution")
                    setError('سوالات شما به اتمام رسیده است. از مشارکت شما سپاس‌گزاریم.')
                else
                    setError('خطایی پیش آمده است.')
            }
            else
                    setError('خطایی پیش آمده است.')
            return jsonData;
        } catch (error) {
            console.log(error);
            return {error: true};
        } finally {
            setIsLoading(false); // Set loading state back to false
        }
    }, [fiValue]);

    const handleNextQuestion = useCallback((next) => {
        if (next)
            fetchFirstQuestion().then();
        else {
            setIsThanks(true)
        }
    }, [fetchFirstQuestion]);

    useEffect(() => {
        if (firstQuestion) {
            setIsQuestion(true);
            setQuestionPage(<QuestionPage username={fiValue} firstQuestion={firstQuestion}
                                          handleQ={handleNextQuestion}/>)
        }
    }, [firstQuestion, fiValue])


    const LampIcon = () => (
        <div className="relative inline-block" data-tooltip-id="tips" data-tooltip-content="سلام. مرسی از وقتی که برامون می‌ذارید.
هدف این پروژه پیدا کردن بهترین روش برای تبدیل فارسی محاوره‌ای به رسمی هست.
به ازای هر یک جمله‌ی غیر رسمی که توسط یک انسان نوشته شده، به ۶ روش مختلف سعی کردیم نسخه‌های رسمیش رو تولید کنیم.
با drag and drop کردن، به ترتیبی که فکر می‌کنید بهترین نسخه‌ها هستند، گزینه‌ها رو مرتب کنید و بعد حتما دکمه‌ی ذخیره رو بزنید.
لطفا دقت داشته باشید که اگر نسخه‌ای زیاد شبیه نسخه‌ی اصلی بود و به حالت رسمی و نوشتاری در نیامده بود (میزان تغییرات کم بود)، این مساله را یک نکته‌ی منفی در نظر بگیرید. همچنین اگر معنی جمله کاملا عوض شده بود نکته‌ی منفی است.">
    <span
        className="text-yellow-500 hover:text-yellow-400 cursor-pointer"
        data-tip="Tooltip text"
    >
      <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="black"
      >
    <path
        d="M 11 0 L 11 3 L 13 3 L 13 0 L 11 0 z M 4.2226562 2.8085938 L 2.8085938 4.2226562 L 4.9296875 6.34375 L 6.34375 4.9296875 L 4.2226562 2.8085938 z M 19.777344 2.8085938 L 17.65625 4.9296875 L 19.070312 6.34375 L 21.191406 4.2226562 L 19.777344 2.8085938 z M 12 5 C 8.1456661 5 5 8.1456661 5 12 C 5 14.767788 6.6561188 17.102239 9 18.234375 L 9 21 C 9 22.093063 9.9069372 23 11 23 L 13 23 C 14.093063 23 15 22.093063 15 21 L 15 18.234375 C 17.343881 17.102239 19 14.767788 19 12 C 19 8.1456661 15.854334 5 12 5 z M 12 7 C 14.773666 7 17 9.2263339 17 12 C 17 14.184344 15.605334 16.022854 13.666016 16.708984 L 13 16.943359 L 13 21 L 11 21 L 11 16.943359 L 10.333984 16.708984 C 8.3946664 16.022854 7 14.184344 7 12 C 7 9.2263339 9.2263339 7 12 7 z M 0 11 L 0 13 L 3 13 L 3 11 L 0 11 z M 21 11 L 21 13 L 24 13 L 24 11 L 21 11 z M 4.9296875 17.65625 L 2.8085938 19.777344 L 4.2226562 21.191406 L 6.34375 19.070312 L 4.9296875 17.65625 z M 19.070312 17.65625 L 17.65625 19.070312 L 19.777344 21.191406 L 21.191406 19.777344 L 19.070312 17.65625 z"></path>
      </svg>
    </span>
            <ReactTooltip variant="info" wrapper='p' float='true' clickable='true'
                          style={{
                              maxWidth: '250px',
                              height: 'auto',
                              fontSize: '9pt',
                              fontWeight: 'normal',
                              lineHeight: '20px'
                          }}
                          id='tips'/>
        </div>
    );


    const handleStartClick = useCallback((event) => {
        event.preventDefault();
        // console.log(email.current.value);
        handleNextQuestion(true);
    }, [username]);
    const StartComponent = () => {
        return (
            <div>
                <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
                    <div className="sm:mx-auto sm:w-full sm:max-w-sm">
                        <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
                            ارزیابی مدل تبدیل فارسی غیر رسمی به رسمی
                            <span>
                                <LampIcon/>
                            </span>
                        </h2>
                    </div>

                    <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                        <form className="space-y-6" onSubmit={handleStartClick}>
                            <div>
                                <label htmlFor="username" className="block text-sm font-medium leading-6 text-gray-900">
                                    نام کاربری
                                </label>
                                <div className="mt-2">
                                    <input
                                        id="username"
                                        name="username"
                                        type="text"
                                        required
                                        ref={username}
                                        className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                    />
                                </div>
                            </div>

                            <div>
                                {isLoading ?
                                    <button
                                        className="disabled flex w-full justify-center rounded-md bg-indigo-100 px-3
                                    py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-100
                                    focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2
                                     focus-visible:outline-indigo-600"
                                    >
                                        در حال پردازش
                                    </button>
                                    :
                                    <button
                                        type="submit"
                                        className="flex w-full justify-center rounded-md bg-indigo-600 px-3
                                    py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500
                                    focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2
                                     focus-visible:outline-indigo-600"
                                        onClick={handleStartClick}
                                    >
                                        شروع ارزیابی
                                    </button>
                                }
                                {error && <div className='rounded-xl bg-red-100 text-red-800 p-2 m-2'>{error}</div>}
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div>
            {(isQuestion && questionPage) ? (
                isThanks ? (<ThanksPage/>) : (questionPage)
            ) : (
                <StartComponent/>
            )}
        </div>
    );
};

export default StartPage;
