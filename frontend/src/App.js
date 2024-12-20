
import { Route, Routes } from 'react-router-dom';
import './App.css';
import Layout from './components/layout/Layout';
import Home from './pages/home/Home';
import Auth from './pages/auth/Auth';

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path='auth' element={<Auth />} />
      </Route>
    </Routes>
  );
}

export default App;
