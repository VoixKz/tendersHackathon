import React, { useState, useEffect } from 'react';
import './Home.css';
import userStore from '../../store/UserStore';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Home = () => {
    const [tenders, setTenders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchTenders = async () => {
            try {
                const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NTM4NDk0LCJpYXQiOjE3MzQ0NTIwOTQsImp0aSI6IjcxNjI1N2VkZmQzYTQwZDFiMzFhZWUxYzJkODMyN2I5IiwiZW1haWwiOiJjdXN0b21lckBleGFtcGxlLmNvbSJ9.WCV8DUt5Ptalw1WUf8xRq4iJQXxsPgts_EYTP-TffuY'
                const axiosInstance = axios.create({
                    baseURL: 'http://127.0.0.1:8000/api/',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                });

                const response = await axiosInstance.get('tenders/');
                console.log(response)
                setTenders(response.data);
                setLoading(false);
            } catch (err) {
                setError(err.message || 'Ошибка при загрузке данных');
                setLoading(false);
            }
        };

        fetchTenders();
    }, []);

    const [selectedTag, setSelectedTag] = useState('');
    const [selectedType, setSelectedType] = useState('');
    const [searchQuery,     setSearchQuery] = useState('');

    const formatDate = (isoString) => {
        const date = new Date(isoString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}.${month}.${year}`;
    };

    const formatPrice = (isoString) => {
        const price = isoString.split()[0];
        return `${price}KZT`;
    };

    const filteredTenders = tenders.filter((tender) => {
        return (
            (!selectedTag || tender.tag === selectedTag) &&
            (!selectedType || tender.type === selectedType) &&
            tender.title.toLowerCase().includes(searchQuery.toLowerCase())
        );
    });

    return (
        <main className="between-start">
            <div className="side-bar">
                <div className="side-bar-block">
                    <p className="side-bar-title">Фильтры</p>
                    <div className="filter-block">
                        <p className="filter-title">Тэги</p>
                        <div className="filter-links">
                            {['Строительство', 'IT и телекоммуникации', 'Здравоохранение', 'Энергетика'].map((tag) => (
                                <div
                                    key={tag}
                                    className={selectedTag === tag ? 'filter-link active' : 'filter-link'}
                                    onClick={() => setSelectedTag(selectedTag === tag ? '' : tag)}
                                >
                                    <div className="circle"></div>
                                    <p className="filter-subtitle">{tag}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="filter-block">
                        <p className="filter-title">Тип</p>
                        <div className="filter-links">
                            {['Государственные закупки', 'Коммерческие тендеры', 'Международные тендеры'].map((type) => (
                                <div
                                    key={type}
                                    className={selectedType === type ? 'filter-link active' : 'filter-link'}
                                    onClick={() => setSelectedType(selectedType === type ? '' : type)}
                                >
                                    <div className="circle"></div>
                                    <p className="filter-subtitle">{type}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            <div className="tenders">
                <header className="tender-header">
                    <nav className="tender-nav">
                        <Link to="#">
                            <img src="" alt="Logo" />
                        </Link>
                        <div className="auth">
                            {userStore.user ? (
                                <div className="auth-info">
                                    <p className="auth-title">{userStore.user.firstName}</p>
                                    <p className="auth-subtitle">{userStore.user.email}</p>
                                </div>
                            ) : (
                                <Link to='/auth'><button className='register-button'>Войти</button></Link>
                            )}
                        </div>
                    </nav>
                </header>

                <div className="search-container">
                    <input
                        type="text"
                        placeholder="Поиск по названию..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="search-input"
                    />
                    <button
                        className="reset-button"
                        onClick={() => {
                            setSearchQuery('');
                            setSelectedTag('');
                            setSelectedType('');
                        }}
                    >
                        Сбросить фильтры
                    </button>
                </div>

                <div className="tender-main">
                    <div className="tender-table-container">
                        {loading ? (
                            <p>Загрузка...</p>
                        ) : error ? (
                            <p className="error">{error}</p>
                        ) : filteredTenders.length > 0 ? (
                            <table className="tender-table">
                                <thead>
                                    <tr>
                                        <th>Название</th>
                                        <th>Описание</th>
                                        <th>Бюджет</th>
                                        <th>Дата открытия тендера</th>
                                        <th>Дедлайн</th>
                                        <th>Хэш блокчейна</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredTenders.map((tender) => (
                                        <tr key={tender.id}>
                                            <td>{tender.title}</td>
                                            <td>{tender.description}</td>
                                            <td>{formatPrice(tender.price)}</td>
                                            <td>{formatDate(tender.start_date)}</td>
                                            <td>{formatDate(tender.end_date)}</td>
                                            <td>{tender.blockchain_tx}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <p className="no-tenders">Нет тендеров для отображения</p>
                        )}
                    </div>
                </div>
            </div>
        </main>
    );
};

export default Home;
