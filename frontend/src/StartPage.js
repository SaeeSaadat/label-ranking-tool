import React, {useCallback, useEffect, useRef, useState} from 'react';
import QuestionPage from "./QuestionPage";
import ThanksPage from "./ThanksPage";

const StartPage = () => {
    const username = useRef('');
    const [fiValue, setFiValue] = useState(null);
    const [isQuestion, setIsQuestion] = useState(false)
    const [isThanks, setIsThanks] = useState(false)
    const [firstQuestion, setFirstQuestion] = useState()
    const [questionPage, setQuestionPage] = useState(null);


    const fetchFirstQuestion = async () => {
        try {
            let response
            if (fiValue) {
                response = await fetch(`${process.env.REACT_APP_API_HOST}/question/` + fiValue);
            } else {
                setFiValue(username.current.value)
                response = await fetch(`${process.env.REACT_APP_API_HOST}/question/` + username.current.value);
            }
            const jsonData = await response.json();
            if (response.ok)
                setFirstQuestion(jsonData);
            return jsonData;
        } catch (error) {
            console.log(error);
            return {error: true};
        }
    };

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
                            ارزیابی مدل تبدیل جملات فارسی غیر رسمی به رسمی
                        </h2>
                    </div>

                    <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                        <form className="space-y-6" onSubmit={handleStartClick}>
                            <div>
                                <p>
                                    سلام. مرسی از وقتی که برامون می‌ذارید.
                                    هدف این پروژه پیدا کردن بهترین روش برای تبدیل فارسی محاوره‌ای به رسمی هست.
                                    به ازای هر یک جمله‌ی غیر رسمی که توسط یک انسان نوشته شده، به ۶ روش مختلف سعی کردیم
                                    نسخه‌های رسمیش رو تولید کنیم.
                                    با drag and drop کردن، به ترتیبی که فکر می‌کنید بهترین نسخه‌ها هستند، گزینه‌ها رو
                                    مرتب کنید و بعد حتما دکمه‌ی ذخیره رو بزنید.
                                    لطفا دقت داشته باشید که اگر نسخه‌ای زیاد شبیه نسخه‌ی اصلی بود و به حالت رسمی و
                                    نوشتاری در نیامده بود (میزان تغییرات کم بود)، این مساله را یک نکته‌ی منفی در نظر
                                    بگیرید. همچنین اگر معنی جمله کاملا عوض شده بود نکته‌ی منفی است.
                                </p>
                                <label htmlFor="email" className="block text-sm font-medium leading-6 text-gray-900">
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
                                <button
                                    type="submit"
                                    className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                    onClick={handleStartClick}
                                >
                                    شروع ارزیابی
                                </button>
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
