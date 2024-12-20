import { useEffect, useState } from 'react';
import './Auth.css';
import axios from 'axios';
import userStore from '../../store/UserStore';
import { useNavigate } from 'react-router-dom';

const Auth = () => {
    const [authType, setAuthType] = useState(0)
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [firstname, setFirstname] = useState('')
    const [lastname, setLastname] = useState('')
    const [phone, setPhone] = useState('')
    const [iin, setIin] = useState('')

    const navigate = useNavigate();

    const handleLogin = async () => {
        navigate('/');
    }

    const handleSignUp = async () => {
        navigate('/');
    }

    const handleClick = () => {
        if (authType === 0) {
            setAuthType(1);
        }

        else {
            setAuthType(0);
        }
    }

    const handleEmail = (e) => {
        setEmail(e.target.value);
    }

    const handleFirstname = (e) => {
        setFirstname(e.target.value);
    }

    const handleLastname = (e) => {
        setLastname(e.target.value);
    }

    const handlePhone = (e) => {
        setPhone(e.target.value);
    }

    const handlePassword = (e) => {
        setPassword(e.target.value);
    }

    const handleIIN = (e) => {
        setIin(e.target.value);
    }

    return (
        <main className='auth-container'>
            <div>
                <div className={authType === 0 ? 'auth-type left' : 'auth-type right'}>
                    {authType === 0 ? <button className='auth-button' onClick={handleClick}>Создать аккаунт</button> : <button className='auth-button' onClick={handleClick}>Войти в аккаунт</button>}
                </div>
                <div className='auth-content'>
                    <p className='auth-title'>Давайте начнем!</p>
                    {authType === 0 ?
                        <>
                            <input className='pink-input' placeholder='Your e-mail' value={email} onChange={handleEmail}></input>
                            <input className='white-input' placeholder='Password' type='password' value={password} onChange={handlePassword}></input>
                            <button className='auth-button' onClick={handleLogin}>Login</button>
                        </>
                        :
                        <>
                            <input className='pink-input' placeholder='Your e-mail'></input>
                            <div className='auth-inputs'>
                                <input className='white-input' placeholder='First name' value={firstname} onChange={handleFirstname}></input>
                                <input className='white-input' placeholder='Last name' value={lastname} onChange={handleLastname}></input>
                            </div>
                            <input className='pink-input' placeholder='Password' value={password} onChange={handlePassword}></input>
                            <input className='white-input' placeholder='Phone number' value={phone} onChange={handlePhone}></input>

                            <p className='input-label'>Individual identification number</p>
                            <input className='pink-input' placeholder='Ex. 061130550327' value={iin} onChange={handleIIN}></input>
                            <button className='auth-button' onClick={handleSignUp}>Sign Up</button>
                        </>}
                </div>
            </div>
        </main>
    )
}

export default Auth;